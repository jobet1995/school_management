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
    
    // Set initial state
    updateCarousel(slider, items, currentIndex);
    
    // Event listeners for navigation
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel(slider, items, currentIndex);
    });
    
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel(slider, items, currentIndex);
    });
    
    // Touch/swipe support
    let startX = 0;
    let endX = 0;
    
    slider.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    });
    
    slider.addEventListener('touchend', (e) => {
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
            updateCarousel(slider, items, currentIndex);
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