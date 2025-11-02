function makeSystemCall(action) {
    fetch('/system_call', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        showModal(data.message, data.success);
    })
    .catch(error => {
        showModal('Error occurred! Please try again.', false);
    });
}

function showModal(message, success) {
    const modal = document.getElementById('resultModal');
    const modalMessage = document.getElementById('modalMessage');
    const modalIcon = document.getElementById('modalIcon');
    
    modalMessage.textContent = message;
    modalIcon.textContent = success ? '✅' : '❌';
    
    modal.style.display = 'block';
    
    // Auto close after 3 seconds
    setTimeout(() => {
        closeModal();
    }, 3000);
}

function closeModal() {
    document.getElementById('resultModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('resultModal');
    if (event.target == modal) {
        closeModal();
    }
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});