document.addEventListener('DOMContentLoaded', function() {
    // Initialize all CTA banner plugins
    const ctaBanners = document.querySelectorAll('.cta-banner');
    ctaBanners.forEach(banner => {
        initializeCTABanner(banner);
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
    
    observer.observe(banner);
}