document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('register-form');
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm-password');
  const passwordStrengthBar = document.getElementById('password-strength-bar');

  function checkPasswordStrength(password) {
    let strength = 0;
    if(password.length >= 8) strength += 25;
    if(password.match(/[A-Z]/)) strength += 25;
    if(password.match(/[0-9]/)) strength += 25;
    if(password.match(/[^A-Za-z0-9]/)) strength += 25;

    passwordStrengthBar.style.width = strength + '%';

    if(strength <= 25) {
      passwordStrengthBar.style.backgroundColor = '#ff4757';
    } else if(strength <= 50) {
      passwordStrengthBar.style.backgroundColor = '#ffa502';
    } else if(strength <= 75) {
      passwordStrengthBar.style.backgroundColor = '#2ed573';
    } else {
      passwordStrengthBar.style.backgroundColor = '#7bed9f';
    }
  }

  password.addEventListener('input', (e) => {
    checkPasswordStrength(e.target.value);
  });

  username.addEventListener('input', (e) => {
    const usernameError = document.getElementById('username-error');
    if (e.target.value.length < 3) {
      usernameError.textContent = 'Username must be at least 3 characters long';
      usernameError.style.display = 'block';
    } else {
      usernameError.style.display = 'none';
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    let isValid = true;

    if(username.value.length < 3) {
      document.getElementById('username-error').textContent = 'Username must be at least 3 characters long';
      document.getElementById('username-error').style.display = 'block';
      isValid = false;
    } else {
      document.getElementById('username-error').style.display = 'none';
    }

    if(password.value.length < 8) {
      document.getElementById('password-error').style.display = 'block';
      isValid = false;
    } else {
      document.getElementById('password-error').style.display = 'none';
    }

    if(password.value !== confirmPassword.value) {
      document.getElementById('confirm-password-error').style.display = 'block';
      isValid = false;
    } else {
      document.getElementById('confirm-password-error').style.display = 'none';
    }

    if(isValid) {

      const userData = {
        username: username.value,
        password: password.value
      };

      const response = await fetch('http://localhost:10001/api/v1/register', { // change URL
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
          mode: "no-cors"
      });

      if (response.ok) {
          window.location.href = 'http://localhost:8000/login'; // change URL
      } else {
          document.getElementById('username-error').textContent = 'Username already exists';
          document.getElementById('username-error').style.display = 'block';
      }
    }
  });
});
