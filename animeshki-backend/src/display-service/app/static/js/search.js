document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
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

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') { 
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                window.location.href = `/search?query=${encodeURIComponent(searchTerm)}`; // change it!!!!
                console.log('Searching for:', searchTerm);
            }
        }
    });
  });