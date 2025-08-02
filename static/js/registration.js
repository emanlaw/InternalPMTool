// Registration Form Validation and Enhancement

document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const submitBtn = document.getElementById('submitBtn');
    const registrationForm = document.getElementById('registrationForm');

    // Password strength validation
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            const strengthDiv = document.getElementById('passwordStrength');
            
            if (password.length === 0) {
                strengthDiv.innerHTML = '';
                return;
            }
            
            let strength = 0;
            if (password.length >= 6) strength++;
            if (password.match(/[a-z]/)) strength++;
            if (password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;
            
            if (strength < 2) {
                strengthDiv.innerHTML = '<span class="strength-weak">Weak password</span>';
            } else if (strength < 4) {
                strengthDiv.innerHTML = '<span class="strength-medium">Medium password</span>';
            } else {
                strengthDiv.innerHTML = '<span class="strength-strong">Strong password</span>';
            }
            
            checkPasswordMatch();
        });
    }

    // Password confirmation validation
    function checkPasswordMatch() {
        if (!passwordField || !confirmPasswordField) return;
        
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        const matchDiv = document.getElementById('passwordMatch');
        
        if (confirmPassword.length === 0) {
            matchDiv.innerHTML = '';
            if (submitBtn) submitBtn.disabled = false;
            return;
        }
        
        if (password === confirmPassword) {
            matchDiv.innerHTML = '<span class="match-success">✓ Passwords match</span>';
            if (submitBtn) submitBtn.disabled = false;
        } else {
            matchDiv.innerHTML = '<span class="match-error">✗ Passwords do not match</span>';
            if (submitBtn) submitBtn.disabled = true;
        }
    }

    if (confirmPasswordField) {
        confirmPasswordField.addEventListener('input', checkPasswordMatch);
    }

    // Form validation on submit
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            const password = passwordField ? passwordField.value : '';
            const confirmPassword = confirmPasswordField ? confirmPasswordField.value : '';
            const email = document.getElementById('email') ? document.getElementById('email').value : '';
            const displayName = document.getElementById('display_name') ? document.getElementById('display_name').value : '';
            const username = document.getElementById('username') ? document.getElementById('username').value : '';
            
            // Validation checks
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
                return false;
            }
            
            if (password.length < 6) {
                e.preventDefault();
                alert('Password must be at least 6 characters long!');
                return false;
            }
            
            if (!email || !email.includes('@')) {
                e.preventDefault();
                alert('Please enter a valid email address!');
                return false;
            }
            
            if (!displayName || displayName.trim().length < 2) {
                e.preventDefault();
                alert('Display name must be at least 2 characters long!');
                return false;
            }
            
            if (!username || username.length < 3) {
                e.preventDefault();
                alert('Username must be at least 3 characters long!');
                return false;
            }
            
            // Show loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating Account...';
            }
        });
    }

    // Email validation
    const emailField = document.getElementById('email');
    if (emailField) {
        emailField.addEventListener('blur', function() {
            const email = this.value;
            if (email && !email.includes('@')) {
                this.style.borderColor = '#ff5630';
            } else {
                this.style.borderColor = '#ddd';
            }
        });
    }

    // Username validation (no spaces, special characters)
    const usernameField = document.getElementById('username');
    if (usernameField) {
        usernameField.addEventListener('input', function() {
            let value = this.value;
            // Remove spaces and special characters except underscore and dash
            value = value.replace(/[^a-zA-Z0-9_-]/g, '');
            this.value = value;
        });
    }
});

// Utility functions for admin notifications
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        ${type === 'success' ? 'background: #36b37e;' : 'background: #ff5630;'}
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);