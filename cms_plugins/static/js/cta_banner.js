(function($) {
    $(document).ready(function() {
        // Initialize all CTA banner plugins
        $('.cta-banner').each(function() {
            initializeCTABanner($(this));
        });
        
        // Handle CTA button clicks
        $(document).on('click', '.cta-button', function(e) {
            const href = $(this).attr('href');
            
            // Check if it's an anchor link
            if (href && href.startsWith('#')) {
                e.preventDefault();
                
                // Get target element
                const target = $(href);
                if (target.length) {
                    // Calculate offset for sticky navbar (adjust as needed)
                    const navbarHeight = $('.navbar').outerHeight() || 0;
                    const scrollTop = target.offset().top - navbarHeight;
                    
                    // Animate scroll with duration based on distance
                    const currentScroll = $(window).scrollTop();
                    const distance = Math.abs(scrollTop - currentScroll);
                    const duration = Math.min(1500, Math.max(500, distance / 3)); // Between 500-1500ms
                    
                    $('html, body').animate({
                        scrollTop: scrollTop
                    }, duration);
                }
            }
        });
        
        // Add hover effect to CTA buttons using CSS classes
        $(document).on('mouseenter', '.cta-button', function() {
            $(this).addClass('hover');
        });
        
        $(document).on('mouseleave', '.cta-button', function() {
            $(this).removeClass('hover');
        });
    });

    function initializeCTABanner(banner) {
        // Add fade-in animation when section comes into view
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
        
        observer.observe(banner[0]);
    }
})(django.jQuery);