# Secure System Call Interface
**Course:** CSE234 — Operating Systems  
**Project:** CA2  
**Author:** Hemant Sihag  
**Registration No.:** 12416315  
**Roll No.:** 3

---

## Project Overview
Secure System Call Interface is a Flask-based web application that provides a **sandboxed, secure** web interface to simulate operating-system-level system calls for educational purposes. The app validates and restricts operations, logs all requests, and displays results on a simple HTML dashboard.

---

## Features
- Secure user authentication (simple login/session)
- Simulated system calls (safe wrappers for operations such as `read`, `write`, `open`)
- Input validation and sanitization to prevent unsafe operations
- Logging/audit of every request (timestamp, user, syscall, result)
- Basic HTML dashboard to run simulations and display results
- Unit tests for key logic (optional)

---

## Repository structure (recommended)
```
project-ca2-os/
├─ code/
│  ├─ app.py                 # Flask application entry
│  ├─ requirements.txt
│  ├─ modules/
│  │  ├─ syscall_validator.py
│  │  ├─ syscall_executor.py
│  │  └─ auth.py
│  └─ templates/
│     ├─ index.html
│     └─ login.html
├─ REPORT_CSE234.pdf
├─ AI_Breakdown.md
├─ Problem_Statement.md
├─ Flow_Diagram.png
├─ README.md
└─ Operating_System.zip
```

---

## Quick setup (local)
> Tested on Python 3.8+ (use a virtualenv)

1. Clone the repository:
```bash
git clone https://github.com/hemantsihag007/project-ca2-os.git
cd project-ca2-os/code
```

2. Create & activate virtual environment (Windows):
```powershell
python -m venv venv
venv\Scripts\activate
```
macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask app (development):
```bash
python app.py
```

5. Open a browser and go to:
```
http://127.0.0.1:5000/
```

---

## Example endpoints / usage
- `GET /` — Dashboard (requires login)  
- `GET /login` — Login page  
- `POST /api/syscall` — Execute a simulated syscall  

Example JSON body:
```json
{
  "operation": "read",
  "target": "sample.txt",
  "mode": "safe"
}
```

---

## Security notes
- This project **does not** execute real kernel syscalls. It *simulates* them in a controlled environment.
- All user inputs are validated and restricted to an allow-list of operations and target paths.
- Logs capture user, operation, timestamp, and result for auditing.

---

## How this meets CA2 submission guidelines (CSE234)
- Repository includes `REPORT_CSE234.pdf`, `AI_Breakdown.md`, `Problem_Statement.md`, and `Flow_Diagram.png`.
- At least **7 commits** showing iterative development.
- Feature branches merged into `main`.
- Screenshot of commit history added in report under *Revision Tracking*.

---

## Helpful Git commands
```bash
git init
git add .
git commit -m "Initial commit: Secure System Call Interface"
git branch -M main
git remote add origin https://github.com/hemantsihag007/project-ca2-os.git
git push -u origin main
```

---

## requirements.txt (example)
```
Flask>=2.0
pytest
```
Add other packages if used (e.g., `flask-login`, `sqlalchemy`).

---

## Final submission checklist
- [ ] Source code uploaded and visible
- [ ] Report and appendices added
- [ ] ≥ 7 commits
- [ ] 1+ feature branches merged
- [ ] Repo link added in report

---

## Contact
For queries, contact **Hemant Sihag (12416315)**.
