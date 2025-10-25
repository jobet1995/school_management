document.addEventListener('DOMContentLoaded', function() {
    // Initialize all welcome section plugins
    const welcomeSections = document.querySelectorAll('.welcome-section');
    welcomeSections.forEach(section => {
        initializeWelcomeSection(section);
    });
});

function initializeWelcomeSection(section) {
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
    
    observer.observe(section);
}