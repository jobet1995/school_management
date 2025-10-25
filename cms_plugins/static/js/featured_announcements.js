document.addEventListener('DOMContentLoaded', function() {
    // Initialize all featured announcements plugins
    const plugins = document.querySelectorAll('.featured-announcements');
    plugins.forEach(plugin => {
        initializePlugin(plugin);
    });
});

function initializePlugin(plugin) {
    const pluginId = plugin.getAttribute('data-plugin-id');
    const container = plugin.querySelector('.announcements-container');
    const list = plugin.querySelector('.announcements-list');
    const prevBtn = plugin.querySelector('.carousel-prev');
    const nextBtn = plugin.querySelector('.carousel-next');
    
    // Check if carousel is enabled
    if (container.classList.contains('carousel-enabled')) {
        initCarousel(plugin, list, prevBtn, nextBtn);
    }
    
    // Initialize read more functionality
    initReadMore(plugin);
    
    // Initialize fade-in animations
    initFadeInAnimations(plugin);
}

function initCarousel(plugin, list, prevBtn, nextBtn) {
    let currentIndex = 0;
    const items = list.querySelectorAll('.announcement-item');
    const totalItems = items.length;
    
    if (totalItems <= 1) return;
    
    // Set initial state
    updateCarousel(list, items, currentIndex);
    
    // Event listeners for navigation
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel(list, items, currentIndex);
    });
    
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel(list, items, currentIndex);
    });
    
    // Touch/swipe support
    let startX = 0;
    let endX = 0;
    
    list.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    });
    
    list.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        handleSwipe(startX, endX);
    });
    
    function handleSwipe(start, end) {
        const threshold = 50;
        const diff = start - end;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Swipe left - next
                currentIndex = (currentIndex + 1) % totalItems;
            } else {
                // Swipe right - previous
                currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            }
            updateCarousel(list, items, currentIndex);
        }
    }
}

function updateCarousel(list, items, index) {
    // Hide all items
    items.forEach(item => {
        item.style.display = 'none';
    });
    
    // Show current item
    items[index].style.display = 'block';
    
    // Add animation class
    items[index].classList.add('carousel-animate');
    setTimeout(() => {
        items[index].classList.remove('carousel-animate');
    }, 300);
}

function initReadMore(plugin) {
    const readMoreButtons = plugin.querySelectorAll('.read-more-btn');
    
    readMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const contentWrapper = this.parentElement;
            const content = contentWrapper.querySelector('.announcement-content');
            const originalContent = content.textContent;
            
            if (this.textContent === 'Read more') {
                // Expand content
                content.textContent = originalContent;
                this.textContent = 'Read less';
            } else {
                // Truncate content
                content.textContent = originalContent.substring(0, 200) + '...';
                this.textContent = 'Read more';
            }
        });
    });
}

function initFadeInAnimations(plugin) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    const items = plugin.querySelectorAll('.announcement-item');
    items.forEach(item => {
        observer.observe(item);
    });
}