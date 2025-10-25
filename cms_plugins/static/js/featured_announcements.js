document.addEventListener('DOMContentLoaded', function() {
    // Initialize all featured announcements plugins
    const plugins = document.querySelectorAll('.featured-announcements');
    plugins.forEach(plugin => {
        initializePlugin(plugin);
    });
});

function initializePlugin(plugin) {
    const pluginId = plugin.getAttribute('data-plugin-id');
    const container = plugin.querySelector('.announcements-container');
    const list = plugin.querySelector('.announcements-list');
    const prevBtn = plugin.querySelector('.carousel-prev');
    const nextBtn = plugin.querySelector('.carousel-next');
    
    // Fetch announcements via AJAX
    fetchAnnouncements(plugin, pluginId, list);
    
    // Check if carousel is enabled
    if (container.classList.contains('carousel-enabled')) {
        initCarousel(plugin, list, prevBtn, nextBtn);
    }
    
    // Initialize read more functionality
    initReadMore(plugin);
}

function fetchAnnouncements(plugin, pluginId, list) {
    // Show loading state
    list.innerHTML = '<div class="loading">Loading announcements...</div>';
    
    // Get CSRF token
    const csrfToken = getCookie('csrftoken');
    
    // Fetch announcements via AJAX
    fetch(`/cms_plugins/featured-announcements/${pluginId}/`, {
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
            
            // Populate announcements
            data.announcements.forEach((announcement, index) => {
                const announcementElement = createAnnouncementElement(announcement, index);
                list.appendChild(announcementElement);
                
                // Add fade-in animation with delay
                setTimeout(() => {
                    announcementElement.classList.add('fade-in');
                }, index * 100);
            });
            
            // Update plugin title if needed
            const titleElement = plugin.querySelector('h2');
            if (titleElement && data.title) {
                titleElement.textContent = data.title;
            }
            
            // Re-initialize read more functionality for new elements
            initReadMore(plugin);
        } else {
            // Show error message
            list.innerHTML = '<div class="error">Failed to load announcements. Please try again later.</div>';
            console.error('Failed to load announcements:', data.error);
        }
    })
    .catch(error => {
        // Show error message
        list.innerHTML = '<div class="error">Failed to load announcements. Please try again later.</div>';
        console.error('Error fetching announcements:', error);
    });
}

function createAnnouncementElement(announcement, index) {
    const div = document.createElement('div');
    div.className = `announcement-item ${announcement.is_featured ? 'featured' : ''}`;
    div.setAttribute('data-announcement-id', announcement.id);
    
    // Truncate content if too long
    const content = announcement.content.length > 200 ? 
        announcement.content.substring(0, 200) + '...' : 
        announcement.content;
    
    div.innerHTML = `
        <h3>${announcement.title}</h3>
        <p class="announcement-date">${announcement.created_at}</p>
        <div class="announcement-content-wrapper">
            <p class="announcement-content">${content}</p>
            ${announcement.content.length > 200 ? '<button class="read-more-btn">Read more</button>' : ''}
        </div>
    `;
    
    return div;
}

function initCarousel(plugin, list, prevBtn, nextBtn) {
    let currentIndex = 0;
    const items = list.querySelectorAll('.announcement-item');
    const totalItems = items.length;
    
    if (totalItems <= 1) return;
    
    // Set initial state
    updateCarousel(list, items, currentIndex);
    
    // Event listeners for navigation
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel(list, items, currentIndex);
    });
    
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel(list, items, currentIndex);
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

function initReadMore(plugin) {
    const readMoreButtons = plugin.querySelectorAll('.read-more-btn');
    
    readMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const announcementItem = this.closest('.announcement-item');
            const announcementId = announcementItem.getAttribute('data-announcement-id');
            const contentWrapper = this.parentElement;
            const contentElement = contentWrapper.querySelector('.announcement-content');
            
            if (this.textContent === 'Read more') {
                // Fetch full content via AJAX
                fetchFullAnnouncement(announcementId, contentElement, this);
            } else {
                // Collapse content with slide-up animation
                collapseContent(contentElement, this);
            }
        });
    });
}

function fetchFullAnnouncement(announcementId, contentElement, button) {
    // Show loading state
    const originalContent = contentElement.textContent;
    contentElement.textContent = 'Loading...';
    
    // Get CSRF token
    const csrfToken = getCookie('csrftoken');
    
    // Fetch full announcement content via AJAX
    fetch(`/cms_plugins/featured-announcements/detail/${announcementId}/`, {
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
            // Expand content with slide-down animation
            expandContent(contentElement, data.announcement.content, button);
        } else {
            // Restore original content and show error
            contentElement.textContent = originalContent;
            console.error('Failed to load full announcement:', data.error);
        }
    })
    .catch(error => {
        // Restore original content and show error
        contentElement.textContent = originalContent;
        console.error('Error fetching full announcement:', error);
    });
}

function expandContent(contentElement, fullContent, button) {
    // Set the full content
    contentElement.textContent = fullContent;
    
    // Change button text to "Show Less"
    button.textContent = 'Show less';
    
    // Apply slide-down animation
    contentElement.style.maxHeight = '0';
    contentElement.style.overflow = 'hidden';
    contentElement.style.transition = 'max-height 0.3s ease';
    
    // Force reflow
    contentElement.offsetHeight;
    
    // Calculate the natural height
    const naturalHeight = contentElement.scrollHeight;
    contentElement.style.maxHeight = naturalHeight + 'px';
    
    // Clean up transition
    setTimeout(() => {
        contentElement.style.maxHeight = 'none';
        contentElement.style.overflow = 'visible';
        contentElement.style.transition = '';
    }, 300);
}

function collapseContent(contentElement, button) {
    // Apply slide-up animation
    contentElement.style.maxHeight = contentElement.scrollHeight + 'px';
    contentElement.style.overflow = 'hidden';
    contentElement.style.transition = 'max-height 0.3s ease';
    
    // Force reflow
    contentElement.offsetHeight;
    
    // Collapse to 3 lines (approx 60px)
    contentElement.style.maxHeight = '60px';
    
    // After animation, truncate content
    setTimeout(() => {
        const truncatedContent = contentElement.textContent.substring(0, 200) + '...';
        contentElement.textContent = truncatedContent;
        contentElement.style.maxHeight = 'none';
        contentElement.style.overflow = 'visible';
        contentElement.style.transition = '';
        button.textContent = 'Read more';
    }, 300);
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