document.addEventListener('DOMContentLoaded', function() {
    const starButtons = document.querySelectorAll('.star-btn');
    const favoriteBtn = document.querySelector('.favorite-btn');
  
    let currentRating = 0; // Переменная для хранения текущего рейтинга
  
    starButtons.forEach(button => {
      button.addEventListener('click', function() {
        const rating = parseInt(this.dataset.rating, 10); // Получаем рейтинг из data-rating
        currentRating = rating; // Сохраняем текущий рейтинг
  
        // Обновляем состояние звёздочек
        updateStars(currentRating);
  
        alert(`Thank you for rating this anime ${rating} stars!`);
      });
  
      // Hover эффект при наведении
      button.addEventListener('mouseenter', function() {
        const rating = parseInt(this.dataset.rating, 10); // Получаем рейтинг из data-rating
        updateStars(rating, true); // Обновляем звёзды для превью
      });
  
      button.addEventListener('mouseleave', function() {
        updateStars(currentRating); // Возвращаемся к текущему рейтингу
      });
    });
  
    // Функция для обновления состояния звёзд
    function updateStars(rating, preview = false) {
      starButtons.forEach(btn => {
        const btnRating = parseInt(btn.dataset.rating, 10); // Рейтинг кнопки
        if (btnRating <= rating) {
          btn.classList.add('active');
          btn.style.color = preview ? '#ffd700' : ''; // Если превью, меняем цвет
        } else {
          btn.classList.remove('active');
          btn.style.color = ''; // Возвращаем дефолтный цвет
        }
      });
    }
  
    // Обработка кнопки "Добавить в избранное"
    favoriteBtn.addEventListener('click', function() {
      this.classList.toggle('active');
      const isFavorite = this.classList.contains('active');
      this.innerHTML = isFavorite
        ? '<i class="fas fa-heart"></i> Added to Favorites'
        : '<i class="fas fa-heart"></i> Add to Favorites';
  
      if (isFavorite) {
        alert('Added to favorites!');
      } else {
        alert('Removed from favorites!');
      }
    });
  });