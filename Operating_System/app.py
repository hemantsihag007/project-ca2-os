from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'mysecretkey123'

USERS_FILE = 'users.json'
LOGS_FILE = 'logs.txt'

# Initialize users.json with more users
def init_users():
    if not os.path.exists(USERS_FILE):
        users = {
            "admin": {"password": "1234", "role": "admin", "full_name": "System Administrator"},
            "user1": {"password": "abcd", "role": "normal", "full_name": "John Doe"},
            "user2": {"password": "pass123", "role": "normal", "full_name": "Jane Smith"}
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

# Initialize logs.txt
def init_logs():
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'w') as f:
            f.write("Username | Action | Result | Timestamp | IP Address\n")
            f.write("-" * 100 + "\n")

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def write_log(username, action, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.remote_addr if request else "Unknown"
    log_entry = f"{username} | {action} | {result} | {timestamp} | {ip_address}\n"
    with open(LOGS_FILE, 'a') as f:
        f.write(log_entry)

def read_logs():
    logs = []
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'r') as f:
            lines = f.readlines()[2:]
            for line in lines:
                if line.strip():
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        logs.append({
                            'username': parts[0],
                            'action': parts[1],
                            'result': parts[2],
                            'timestamp': parts[3],
                            'ip': parts[4] if len(parts) > 4 else 'N/A'
                        })
    return logs

# Get statistics for dashboard
def get_stats():
    logs = read_logs()
    total_actions = len(logs)
    success_count = sum(1 for log in logs if log['result'] == 'Success')
    denied_count = sum(1 for log in logs if log['result'] == 'Denied')
    
    # Count actions by type
    action_counts = {}
    for log in logs:
        action = log['action']
        if action not in action_counts:
            action_counts[action] = 0
        action_counts[action] += 1
    
    return {
        'total': total_actions,
        'success': success_count,
        'denied': denied_count,
        'actions': action_counts
    }

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for admin only
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

init_users()
init_logs()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            session['full_name'] = users[username]['full_name']
            write_log(username, "Login", "Success")
            flash(f'Welcome back, {users[username]["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            write_log(username if username else "Unknown", "Login", "Failed")
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    stats = get_stats()
    return render_template('dashboard.html', 
                         username=session['username'], 
                         role=session['role'],
                         full_name=session.get('full_name', 'User'),
                         stats=stats)

@app.route('/system_call', methods=['POST'])
@login_required
def system_call():
    action = request.json.get('action')
    username = session['username']
    role = session['role']
    
    normal_user_actions = ['Open File', 'Read File']
    
    if role == 'admin':
        result = 'Success'
        message = f'{action} completed successfully!'
    elif role == 'normal' and action in normal_user_actions:
        result = 'Success'
        message = f'{action} completed successfully!'
    else:
        result = 'Denied'
        message = f'Access Denied! You do not have permission to perform: {action}'
    
    write_log(username, action, result)
    
    return jsonify({'success': result == 'Success', 'message': message})

@app.route('/logs')
@login_required
def logs():
    log_entries = read_logs()
    # Reverse to show recent logs first
    log_entries.reverse()
    return render_template('logs.html', logs=log_entries, role=session.get('role'))

@app.route('/clear_logs', methods=['POST'])
@admin_required
def clear_logs():
    init_logs()  # Reinitialize logs file
    write_log(session['username'], "Clear All Logs", "Success")
    flash('All logs cleared successfully!', 'success')
    return redirect(url_for('logs'))

@app.route('/statistics')
@login_required
def statistics():
    stats = get_stats()
    logs = read_logs()
    
    # Get recent activities (last 10)
    recent_logs = logs[-10:] if len(logs) > 10 else logs
    recent_logs.reverse()
    
    # User activity summary
    user_activity = {}
    for log in logs:
        user = log['username']
        if user not in user_activity:
            user_activity[user] = {'total': 0, 'success': 0, 'denied': 0}
        user_activity[user]['total'] += 1
        if log['result'] == 'Success':
            user_activity[user]['success'] += 1
        elif log['result'] == 'Denied':
            user_activity[user]['denied'] += 1
    
    return render_template('statistics.html', 
                         stats=stats, 
                         recent_logs=recent_logs,
                         user_activity=user_activity,
                         role=session.get('role'))

@app.route('/profile')
@login_required
def profile():
    users = load_users()
    user_data = users.get(session['username'], {})
    
    # Get user's activity
    logs = read_logs()
    user_logs = [log for log in logs if log['username'] == session['username']]
    
    user_stats = {
        'total_actions': len(user_logs),
        'successful': sum(1 for log in user_logs if log['result'] == 'Success'),
        'denied': sum(1 for log in user_logs if log['result'] == 'Denied'),
        'last_login': user_logs[-1]['timestamp'] if user_logs else 'N/A'
    }
    
    return render_template('profile.html', 
                         user_data=user_data,
                         user_stats=user_stats,
                         username=session['username'])

@app.route('/help')
@login_required
def help_page():
    return render_template('help.html', role=session.get('role'))

@app.route('/logout')
@login_required
def logout():
    username = session.get('username', 'Unknown')
    write_log(username, "Logout", "Success")
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)