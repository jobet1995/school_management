(function($) {
    $(document).ready(function() {
        // Initialize all statistics counter plugins
        $('.statistics-counter-container').each(function() {
            const container = $(this);
            initializeCounter(container);
        });
    });

    function initializeCounter(container) {
        const counters = container.find('.statistics-counter-value');
        
        // Add data attribute to store original values
        counters.each(function() {
            const value = parseInt($(this).text());
            $(this).attr('data-value', value);
            // Set initial value to 0 for animation
            $(this).text('0');
        });
        
        // Add fade-in animation when section comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const container = $(entry.target);
                    animateCounters(container);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        observer.observe(container[0]);
    }

    function animateCounters(container) {
        const counters = container.find('.statistics-counter-value');
        
        counters.each(function() {
            const counter = $(this);
            const target = parseInt(counter.attr('data-value'));
            const duration = 2000; // Animation duration in milliseconds
            const increment = target / (duration / 16); // 16ms per frame (~60fps)
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    clearInterval(timer);
                    counter.text(target.toLocaleString());
                } else {
                    counter.text(Math.ceil(current).toLocaleString());
                }
            }, 16);
        });
    }
})(django.jQuery);