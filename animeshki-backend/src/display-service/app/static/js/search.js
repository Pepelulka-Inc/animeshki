document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const animeCards = document.querySelectorAll('.anime-card');
  
    searchInput.addEventListener('input', function(e) {
      const searchTerm = e.target.value.toLowerCase();
      
      animeCards.forEach(card => {
        const title = card.querySelector('.anime-title').textContent.toLowerCase();
        if (title.includes(searchTerm)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  
    // Add hover effects
    animeCards.forEach(card => {
      card.addEventListener('mouseover', function() {
        this.style.transform = 'translateY(-10px)';
      });
      
      card.addEventListener('mouseout', function() {
        this.style.transform = 'translateY(0)';
      });
    });
  });