document.addEventListener('DOMContentLoaded', function() {
    // Initialize all testimonial plugins
    const testimonialContainers = document.querySelectorAll('.testimonial-container');
    testimonialContainers.forEach(container => {
        initializeTestimonialCarousel(container);
    });
});

function initializeTestimonialCarousel(container) {
    const slider = container.querySelector('.testimonial-slider');
    const items = container.querySelectorAll('.testimonial-item');
    const totalItems = items.length;
    
    if (totalItems <= 1) return;
    
    // Add navigation buttons
    const prevBtn = document.createElement('button');
    prevBtn.className = 'testimonial-nav testimonial-prev';
    prevBtn.innerHTML = '&#8249;';
    prevBtn.setAttribute('aria-label', 'Previous testimonial');
    
    const nextBtn = document.createElement('button');
    nextBtn.className = 'testimonial-nav testimonial-next';
    nextBtn.innerHTML = '&#8250;';
    nextBtn.setAttribute('aria-label', 'Next testimonial');
    
    container.appendChild(prevBtn);
    container.appendChild(nextBtn);
    
    let currentIndex = 0;
    let rotationInterval;
    const rotationDelay = 5000; // 5 seconds
    
    // Set initial state
    updateCarousel(slider, items, currentIndex);
    
    // Start automatic rotation
    startRotation();
    
    // Event listeners for navigation
    prevBtn.addEventListener('click', () => {
        goToPrev();
    });
    
    nextBtn.addEventListener('click', () => {
        goToNext();
    });
    
    // Touch/swipe support
    let startX = 0;
    let endX = 0;
    
    slider.addEventListener('touchstart', (e) => {
        pauseRotation();
        startX = e.touches[0].clientX;
    });
    
    slider.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        handleSwipe(startX, endX);
        startRotation();
    });
    
    // Pause rotation on hover
    container.addEventListener('mouseenter', () => {
        pauseRotation();
    });
    
    container.addEventListener('mouseleave', () => {
        startRotation();
    });
    
    function handleSwipe(start, end) {
        const threshold = 50;
        const diff = start - end;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Swipe left - next
                goToNext();
            } else {
                // Swipe right - previous
                goToPrev();
            }
        }
    }
    
    function goToPrev() {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel(slider, items, currentIndex);
    }
    
    function goToNext() {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel(slider, items, currentIndex);
    }
    
    function startRotation() {
        // Clear any existing interval
        if (rotationInterval) {
            clearInterval(rotationInterval);
        }
        
        // Start new interval
        rotationInterval = setInterval(() => {
            goToNext();
        }, rotationDelay);
    }
    
    function pauseRotation() {
        if (rotationInterval) {
            clearInterval(rotationInterval);
            rotationInterval = null;
        }
    }
    
    // Add fade-in animation when items come into view
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
    
    items.forEach(item => {
        observer.observe(item);
    });
}

function updateCarousel(slider, items, index) {
    // Hide all items with fade-out effect
    items.forEach(item => {
        item.style.opacity = '0';
        item.style.transition = 'opacity 0.5s ease';
    });
    
    // Show current item with fade-in effect
    setTimeout(() => {
        items[index].style.opacity = '1';
    }, 300);
}