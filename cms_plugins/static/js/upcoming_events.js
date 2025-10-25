document.addEventListener('DOMContentLoaded', function() {
    // Initialize all upcoming events plugins
    const plugins = document.querySelectorAll('.upcoming-events');
    plugins.forEach(plugin => {
        initializePlugin(plugin);
    });
});

function initializePlugin(plugin) {
    const pluginId = plugin.getAttribute('data-plugin-id');
    const autoRotate = plugin.getAttribute('data-auto-rotate') === 'true';
    const rotationInterval = parseInt(plugin.getAttribute('data-rotation-interval')) || 5000;
    const container = plugin.querySelector('.events-container');
    const list = plugin.querySelector('.events-list');
    const prevBtn = plugin.querySelector('.carousel-prev');
    const nextBtn = plugin.querySelector('.carousel-next');
    
    // Check if carousel is enabled
    if (container.classList.contains('carousel-enabled')) {
        initCarousel(plugin, list, prevBtn, nextBtn, autoRotate, rotationInterval);
    }
    
    // Initialize countdown timers
    initCountdownTimers(plugin);
}

function initCarousel(plugin, list, prevBtn, nextBtn, autoRotate, rotationInterval) {
    let currentIndex = 0;
    const items = list.querySelectorAll('.event-item');
    const totalItems = items.length;
    let autoRotateInterval;
    
    if (totalItems <= 1) return;
    
    // Set initial state
    updateCarousel(list, items, currentIndex);
    
    // Event listeners for navigation
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel(list, items, currentIndex);
        resetAutoRotate();
    });
    
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel(list, items, currentIndex);
        resetAutoRotate();
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
            resetAutoRotate();
        }
    }
    
    // Auto rotation
    if (autoRotate) {
        startAutoRotate();
    }
    
    function startAutoRotate() {
        autoRotateInterval = setInterval(() => {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel(list, items, currentIndex);
        }, rotationInterval);
    }
    
    function resetAutoRotate() {
        if (autoRotateInterval) {
            clearInterval(autoRotateInterval);
        }
        if (autoRotate) {
            startAutoRotate();
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

function initCountdownTimers(plugin) {
    const timers = plugin.querySelectorAll('.countdown-timer');
    
    timers.forEach(timer => {
        const eventId = timer.getAttribute('data-event-id');
        const eventItem = timer.closest('.event-item');
        const eventStart = new Date(eventItem.getAttribute('data-event-start')).getTime();
        
        // Update countdown immediately
        updateCountdown(timer, eventStart);
        
        // Update countdown every second
        setInterval(() => {
            updateCountdown(timer, eventStart);
        }, 1000);
    });
}

function updateCountdown(timer, eventStart) {
    const now = new Date().getTime();
    const distance = eventStart - now;
    
    if (distance < 0) {
        timer.innerHTML = "Event started!";
        return;
    }
    
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    timer.querySelector('.countdown-days').textContent = days.toString().padStart(2, '0');
    timer.querySelector('.countdown-hours').textContent = hours.toString().padStart(2, '0');
    timer.querySelector('.countdown-minutes').textContent = minutes.toString().padStart(2, '0');
    timer.querySelector('.countdown-seconds').textContent = seconds.toString().padStart(2, '0');
}