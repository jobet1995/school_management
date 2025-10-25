// Scroll-triggered animations for the Student Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations
    initScrollAnimations();
    initCounterAnimations();
});

// Initialize scroll animations
function initScrollAnimations() {
    // Create observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -100px 0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    const animatedElements = document.querySelectorAll(
        '.fade-in, .fade-in-up, .fade-in-down, .fade-in-left, .fade-in-right, .scale-in'
    );
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// Initialize counter animations
function initCounterAnimations() {
    const counters = document.querySelectorAll('.counter');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = parseInt(counter.getAttribute('data-duration')) || 2000;
                const increment = target / (duration / 16); // 16ms per frame (~60fps)
                let current = 0;
                
                counter.classList.add('counting');
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        clearInterval(timer);
                        counter.textContent = target.toLocaleString();
                    } else {
                        counter.textContent = Math.ceil(current).toLocaleString();
                    }
                }, 16);
                
                counterObserver.unobserve(counter);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -100px 0px',
        threshold: 0.1
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Utility function to trigger animations manually
function triggerAnimation(element, animationClass) {
    element.classList.add(animationClass);
    
    // Remove animation class after it completes
    const duration = parseFloat(getComputedStyle(element).transitionDuration) * 1000;
    setTimeout(() => {
        element.classList.remove(animationClass);
    }, duration);
}

// Utility function to add staggered animations to a container
function initStaggeredAnimation(container, animationType = 'fade-in-up') {
    const items = container.children;
    container.classList.add('staggered-animation');
    container.classList.add(`staggered-${items.length}`);
    
    for (let i = 0; i < items.length; i++) {
        items[i].classList.add(animationType);
    }
}

// Export functions for global use
window.initScrollAnimations = initScrollAnimations;
window.initCounterAnimations = initCounterAnimations;
window.triggerAnimation = triggerAnimation;
window.initStaggeredAnimation = initStaggeredAnimation;