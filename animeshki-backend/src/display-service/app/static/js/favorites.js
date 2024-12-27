document.addEventListener('DOMContentLoaded', function() {
    const favoritesGrid = document.querySelector('.favorites-grid');
    const emptyMessage = document.querySelector('.empty-favorites');
    const deleteButtons = document.querySelectorAll('.delete-btn');
  
    deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
        const card = this.closest('.anime-card');
        card.style.transform = 'scale(0.8)';
        card.style.opacity = '0';
        
        setTimeout(() => {
          card.remove();
          checkEmpty();
        }, 300);
      });
    });
  
    function checkEmpty() {
      if (favoritesGrid.children.length === 0) {
        emptyMessage.style.display = 'block';
      } else {
        emptyMessage.style.display = 'none';
      }
    }
  
    // Add hover effects
    const animeCards = document.querySelectorAll('.anime-card');
    animeCards.forEach(card => {
      card.addEventListener('mouseover', function() {
        this.style.transform = 'translateY(-10px)';
      });
      
      card.addEventListener('mouseout', function() {
        this.style.transform = 'translateY(0)';
      });

      card.addEventListener('click', () => {
        window.location.href = '/anime'
      })
    });
  });