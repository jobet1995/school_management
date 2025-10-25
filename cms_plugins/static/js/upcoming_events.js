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
    const showCategoryFilter = plugin.getAttribute('data-show-category-filter') === 'true';
    const showDateFilter = plugin.getAttribute('data-show-date-filter') === 'true';
    const container = plugin.querySelector('.events-container');
    const list = plugin.querySelector('.events-list');
    const prevBtn = plugin.querySelector('.carousel-prev');
    const nextBtn = plugin.querySelector('.carousel-next');
    const categoryFilter = plugin.querySelector('.filter-category');
    const dateFilter = plugin.querySelector('.filter-date');
    const resetFilter = plugin.querySelector('.filter-reset');
    
    // Fetch events via AJAX
    fetchEvents(plugin, pluginId, list, '', '');
    
    // Check if carousel is enabled
    if (container.classList.contains('carousel-enabled')) {
        initCarousel(plugin, list, prevBtn, nextBtn, autoRotate, rotationInterval);
    }
    
    // Initialize filter event listeners
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const category = this.value;
            const date = dateFilter ? dateFilter.value : '';
            fetchEvents(plugin, pluginId, list, category, date);
        });
    }
    
    if (dateFilter) {
        dateFilter.addEventListener('change', function() {
            const date = this.value;
            const category = categoryFilter ? categoryFilter.value : '';
            fetchEvents(plugin, pluginId, list, category, date);
        });
    }
    
    if (resetFilter) {
        resetFilter.addEventListener('click', function() {
            if (categoryFilter) categoryFilter.value = '';
            if (dateFilter) dateFilter.value = '';
            fetchEvents(plugin, pluginId, list, '', '');
        });
    }
}

function fetchEvents(plugin, pluginId, list, category, dateFilter) {
    // Show loading state
    list.innerHTML = '<div class="loading">Loading events...</div>';
    
    // Get CSRF token
    const csrfToken = getCookie('csrftoken');
    
    // Build URL with query parameters
    let url = `/cms-plugins/upcoming-events/${pluginId}/`;
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (dateFilter) params.append('date_filter', dateFilter);
    if (params.toString()) url += '?' + params.toString();
    
    // Fetch events via AJAX
    fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Clear loading state
            list.innerHTML = '';
            
            // Populate events
            if (data.events && data.events.length > 0) {
                data.events.forEach((event, index) => {
                    const eventElement = createEventElement(event);
                    list.appendChild(eventElement);
                    
                    // Add fade-in animation with delay
                    setTimeout(() => {
                        eventElement.classList.add('fade-in');
                    }, index * 100);
                });
                
                // Update plugin title if needed
                const titleElement = plugin.querySelector('h2');
                if (titleElement && data.title) {
                    titleElement.textContent = data.title;
                }
                
                // Reinitialize carousel if enabled
                const container = plugin.querySelector('.events-container');
                if (container.classList.contains('carousel-enabled')) {
                    const prevBtn = plugin.querySelector('.carousel-prev');
                    const nextBtn = plugin.querySelector('.carousel-next');
                    const autoRotate = data.auto_rotate;
                    const rotationInterval = data.rotation_interval;
                    initCarousel(plugin, list, prevBtn, nextBtn, autoRotate, rotationInterval);
                }
                
                // Initialize countdown timers
                initCountdownTimers(plugin);
            } else {
                list.innerHTML = '<div class="no-events">No events found matching the selected filters.</div>';
            }
        } else {
            // Show error message
            list.innerHTML = '<div class="error">Failed to load events. Please try again later.</div>';
            console.error('Failed to load events:', data.error);
        }
    })
    .catch(error => {
        // Show error message
        list.innerHTML = '<div class="error">Failed to load events. Please try again later.</div>';
        console.error('Error fetching events:', error);
    });
}

function createEventElement(event) {
    const div = document.createElement('div');
    div.className = 'event-item';
    div.setAttribute('data-event-id', event.id);
    
    // Format the event dates for countdown timer
    // In a real implementation, we would need the actual datetime values
    // For now, we'll use a placeholder
    const eventStart = new Date(); // This should be the actual event start date
    
    div.innerHTML = `
        <h3>${event.title}</h3>
        <p class="event-dates">
            <span class="start-date">${event.start_date}</span>
            ${event.end_date ? `- <span class="end-date">${event.end_date}</span>` : ''}
        </p>
        ${event.location ? `<p class="event-location">${event.location}</p>` : ''}
        <p class="event-description">${event.description.substring(0, 200)}${event.description.length > 200 ? '...' : ''}</p>
        <div class="event-category ${event.category_key}">${event.category}</div>
        <div class="countdown-timer" data-event-id="${event.id}">
            <span class="countdown-days">00</span>d 
            <span class="countdown-hours">00</span>h 
            <span class="countdown-minutes">00</span>m 
            <span class="countdown-seconds">00</span>s
        </div>
    `;
    
    return div;
}

function initCarousel(plugin, list, prevBtn, nextBtn, autoRotate, rotationInterval) {
    // Clear any existing carousel state
    if (plugin.carouselState) {
        if (plugin.carouselState.autoRotateInterval) {
            clearInterval(plugin.carouselState.autoRotateInterval);
        }
    }
    
    let currentIndex = 0;
    const items = list.querySelectorAll('.event-item');
    const totalItems = items.length;
    let autoRotateInterval;
    
    if (totalItems <= 1) return;
    
    // Set initial state
    updateCarousel(list, items, currentIndex);
    
    // Event listeners for navigation
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            updateCarousel(list, items, currentIndex);
            resetAutoRotate();
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel(list, items, currentIndex);
            resetAutoRotate();
        });
    }
    
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
    
    // Auto-rotation
    if (autoRotate) {
        autoRotateInterval = setInterval(() => {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel(list, items, currentIndex);
        }, rotationInterval);
    }
    
    // Store carousel state
    plugin.carouselState = {
        autoRotateInterval: autoRotateInterval
    };
    
    // Pause auto-rotation on hover
    list.addEventListener('mouseenter', () => {
        if (autoRotateInterval) {
            clearInterval(autoRotateInterval);
        }
    });
    
    list.addEventListener('mouseleave', () => {
        if (autoRotate) {
            autoRotateInterval = setInterval(() => {
                currentIndex = (currentIndex + 1) % totalItems;
                updateCarousel(list, items, currentIndex);
            }, rotationInterval);
            
            // Update carousel state
            plugin.carouselState.autoRotateInterval = autoRotateInterval;
        }
    });
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

function resetAutoRotate() {
    // This function would reset the auto-rotation timer
    // Implementation depends on specific requirements
}

function initCountdownTimers(plugin) {
    // Initialize countdown timers for events
    const countdownTimers = plugin.querySelectorAll('.countdown-timer');
    
    countdownTimers.forEach(timer => {
        const eventId = timer.getAttribute('data-event-id');
        // In a real implementation, you would have the actual event start date
        // For now, we'll just update with placeholder values
        updateCountdownTimer(timer, eventId);
    });
}

function updateCountdownTimer(timer, eventId) {
    // Update the countdown timer
    // This is a simplified implementation
    // In a real application, you would calculate the time remaining until the event
    
    // For demonstration purposes, we'll just show placeholder values
    const daysElement = timer.querySelector('.countdown-days');
    const hoursElement = timer.querySelector('.countdown-hours');
    const minutesElement = timer.querySelector('.countdown-minutes');
    const secondsElement = timer.querySelector('.countdown-seconds');
    
    if (daysElement) daysElement.textContent = '05';
    if (hoursElement) hoursElement.textContent = '12';
    if (minutesElement) minutesElement.textContent = '30';
    if (secondsElement) secondsElement.textContent = '45';
    
    // In a real implementation, you would set up an interval to update the timer
    // and calculate the actual time remaining
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}