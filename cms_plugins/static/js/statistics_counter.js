document.addEventListener('DOMContentLoaded', function() {
    // Initialize all statistics counter plugins
    const counterContainers = document.querySelectorAll('.statistics-counter-container');
    counterContainers.forEach(container => {
        initializeCounter(container);
    });
});

function initializeCounter(container) {
    const counters = container.querySelectorAll('.statistics-counter-value');
    
    // Add data attribute to store original values
    counters.forEach(counter => {
        const value = parseInt(counter.textContent);
        counter.setAttribute('data-value', value);
        // Set initial value to 0 for animation
        counter.textContent = '0';
    });
    
    // Add fade-in animation when section comes into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters(container);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    observer.observe(container);
}

function animateCounters(container) {
    const counters = container.querySelectorAll('.statistics-counter-value');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-value'));
        const duration = 2000; // Animation duration in milliseconds
        const increment = target / (duration / 16); // 16ms per frame (~60fps)
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(timer);
                counter.textContent = target.toLocaleString();
            } else {
                counter.textContent = Math.ceil(current).toLocaleString();
            }
        }, 16);
    });
}