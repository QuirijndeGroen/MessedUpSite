// Handle deregistration without page reload
document.addEventListener('DOMContentLoaded', function() {
    const deregisterForms = document.querySelectorAll('.deregister-form');
    
    deregisterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const registrationListId = this.dataset.registrationlistId;
            const url = this.action;
            const registrationDiv = document.getElementById(registrationListId);
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Hide the deregistration message and button
                    const registeredDiv = registrationDiv.querySelector('.user-registered');
                    if (registeredDiv) {
                        registeredDiv.style.display = 'none';
                    }
                    
                    // Show the registration form
                    const registrationForm = registrationDiv.querySelector('.registration-form-container');
                    if (registrationForm) {
                        registrationForm.style.display = 'block';
                    }
                    
                    // Show success message
                    showMessage('You have been successfully deregistered from this activity.', 'success');
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('An error occurred while deregistering. Please try again.', 'error');
            });
        });
    });
});

// Helper function to show messages
function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 5px;
        z-index: 1000;
        animation: slideIn 0.3s ease-in;
    `;
    
    document.body.appendChild(messageDiv);
    
    // Remove message after 3 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}
