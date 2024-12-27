document.addEventListener('DOMContentLoaded', function() {
    const starButtons = document.querySelectorAll('.star-btn');
    const favoriteBtn = document.querySelector('.favorite-btn');
  
    let currentRating = 0; 
  
    starButtons.forEach(button => {
      button.addEventListener('click', function() {
        const rating = parseInt(this.dataset.rating, 10); 
        currentRating = rating; 
  
        
        updateStars(currentRating);
  
        alert(`Thank you for rating this anime ${rating} stars!`);
      });
  
      button.addEventListener('mouseenter', function() {
        const rating = parseInt(this.dataset.rating, 10); 
        updateStars(rating, true); 
      });
  
      button.addEventListener('mouseleave', function() {
        updateStars(currentRating);
      });
    });
  
    
    function updateStars(rating, preview = false) {
      starButtons.forEach(btn => {
        const btnRating = parseInt(btn.dataset.rating, 10);
        if (btnRating <= rating) {
          btn.classList.add('active');
          btn.style.color = preview ? '#ffd700' : ''; 
        } else {
          btn.classList.remove('active');
          btn.style.color = ''; 
        }
      });
    }
  
    
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

  const commentForm = document.querySelector('.comment-form');
  const commentsContainer = document.querySelector('.comments');

  commentForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const textarea = this.querySelector('textarea');
    const comment = textarea.value.trim();

    if(comment) {
      const newComment = document.createElement('div');
      newComment.className = 'comment';
      newComment.innerHTML = `
        <strong>You</strong>
        <p>${comment}</p>
      `;
      commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
      textarea.value = '';
    }
  });

  });