document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('.login-form');
  const errorMessage = document.getElementById('error-message');
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://localhost:10001/api/v1/login', { // change URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        window.location.href = 'http://localhost:8000/'; // change URL
      } else {
        const data = await response.json();
        errorMessage.textContent = data.message || 'Invalid username or password';
        errorMessage.classList.add('visible');
      }
    } catch (err) {
      errorMessage.textContent = 'Something went wrong. Please try again later.';
      errorMessage.classList.add('visible');
    }
  });
});