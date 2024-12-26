document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.anime-card');
    cards.forEach(card => {
      card.addEventListener('mouseover', function() {
        this.style.transform = 'translateY(-10px)';
      });
      card.addEventListener('mouseout', function() {
        this.style.transform = 'translateY(0)';
      });
    });
  
    const searchBtn = document.querySelector('.search-btn');
    const searchContainer = document.querySelector('.search-container');
    const searchInput = document.querySelector('.search-input');
  
    searchBtn.addEventListener('click', () => {
      searchContainer.classList.toggle('active');
      if (searchContainer.classList.contains('active')) {
        searchInput.focus();
      }
    });
  
    document.addEventListener('click', (e) => {
      if (!searchContainer.contains(e.target) && !searchBtn.contains(e.target)) {
        searchContainer.classList.remove('active');
      }
    });
  
    searchInput.addEventListener('input', (e) => {
      const searchTerm = e.target.value.toLowerCase();
      console.log('Searching for:', searchTerm);
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') { // Проверяем, нажата ли клавиша Enter
            const searchTerm = searchInput.value.trim(); // Получаем текст из поля ввода
            if (searchTerm) {
                // Перенаправляем пользователя на новую страницу с передачей параметра запроса
                // window.location.href = `/search?query=${encodeURIComponent(searchTerm)}`;
                console.log('Searching for:', searchTerm);
            }
        }
    });
  });