(function($) {
    $(document).ready(function() {
        // Initialize all live notifications plugins
        $('.live-notifications').each(function() {
            initializeLiveNotifications($(this));
        });
    });

    function initializeLiveNotifications(container) {
        const pluginId = container.data('plugin-id');
        const toggleBtn = container.find('.notifications-toggle');
        const panel = container.find('.notifications-panel');
        const markAllReadBtn = container.find('.mark-all-read');
        const markReadButtons = container.find('.mark-read');
        
        // Try to establish WebSocket connection if user is authenticated
        let ws = null;
        const userId = container.data('user-id');
        
        if (userId) {
            try {
                // Create WebSocket connection
                const wsUrl = `ws://${window.location.host}/ws/notifications/${userId}/`;
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    console.log('WebSocket connection established');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'notification_update') {
                        // Update UI with new notification
                        updateNotificationsList(container, [data.data]);
                        updateUnreadCount(container);
                    }
                };
                
                ws.onclose = function(event) {
                    console.log('WebSocket connection closed');
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            } catch (e) {
                console.error('Failed to establish WebSocket connection:', e);
            }
        }
        
        // Toggle notifications panel
        toggleBtn.on('click', function(e) {
            e.stopPropagation();
            panel.toggleClass('show');
            toggleBtn.attr('aria-expanded', panel.hasClass('show'));
            panel.attr('aria-hidden', !panel.hasClass('show'));
        });
        
        // Close panel when clicking outside
        $(document).on('click', function(e) {
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                panel.removeClass('show');
                toggleBtn.attr('aria-expanded', 'false');
                panel.attr('aria-hidden', 'true');
            }
        });
        
        // Mark individual notification as read
        markReadButtons.on('click', function(e) {
            e.stopPropagation();
            const notificationItem = $(this).closest('.notification-item');
            const notificationId = notificationItem.data('notification-id');
            
            markNotificationAsRead(notificationId, notificationItem, container, ws);
        });
        
        // Mark all notifications as read
        markAllReadBtn.on('click', function(e) {
            e.stopPropagation();
            const unreadNotifications = container.find('.notification-item.unread');
            
            // Mark each notification as read
            unreadNotifications.each(function() {
                const notificationItem = $(this);
                const notificationId = notificationItem.data('notification-id');
                markNotificationAsRead(notificationId, notificationItem, container, ws);
            });
        });
        
        // Auto-refresh notifications periodically (every 30 seconds)
        setInterval(function() {
            refreshNotifications(pluginId, container);
        }, 30000);
    }
    
    function markNotificationAsRead(notificationId, notificationItem, container, ws) {
        // Make AJAX request to mark notification as read
        $.ajax({
            url: `/cms_plugins/mark-notification-as-read/${notificationId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    // Update UI
                    notificationItem.removeClass('unread');
                    notificationItem.find('.mark-read').remove();
                    
                    // Update unread count
                    updateUnreadCount(container);
                    
                    // Send WebSocket message if connected
                    if (ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({
                            type: 'notification_read',
                            notification_id: notificationId
                        }));
                    }
                } else {
                    console.error('Error marking notification as read:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
            }
        });
    }
    
    function refreshNotifications(pluginId, container) {
        // Make AJAX request to get updated notifications
        $.ajax({
            url: `/cms_plugins/live-notifications/${pluginId}/`,
            method: 'GET',
            success: function(response) {
                if (response.success) {
                    // Update unread count
                    const unreadCount = response.unread_count;
                    const unreadCountElement = container.find('.unread-count');
                    
                    if (unreadCount > 0) {
                        if (unreadCountElement.length) {
                            unreadCountElement.text(unreadCount);
                        } else {
                            container.find('.notifications-toggle').append(
                                `<span class="unread-count">${unreadCount}</span>`
                            );
                        }
                    } else {
                        unreadCountElement.remove();
                    }
                    
                    // Update notifications list if panel is visible
                    const panel = container.find('.notifications-panel');
                    if (panel.hasClass('show')) {
                        updateNotificationsList(container, response.notifications);
                    }
                } else {
                    console.error('Error refreshing notifications:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
            }
        });
    }
    
    function updateUnreadCount(container) {
        // Get current unread count from UI elements
        const unreadCount = container.find('.notification-item.unread').length;
        const unreadCountElement = container.find('.unread-count');
        
        if (unreadCount > 0) {
            if (unreadCountElement.length) {
                unreadCountElement.text(unreadCount);
            } else {
                container.find('.notifications-toggle').append(
                    `<span class="unread-count">${unreadCount}</span>`
                );
            }
        } else {
            unreadCountElement.remove();
        }
    }
    
    function updateNotificationsList(container, notifications) {
        const notificationsList = container.find('.notifications-list');
        let notificationsHtml = '';
        
        if (notifications.length > 0) {
            notifications.forEach(function(notification) {
                const unreadClass = notification.is_read ? '' : 'unread';
                const markReadButton = notification.is_read ? '' : 
                    '<button class="mark-read" aria-label="Mark as read">✓</button>';
                
                notificationsHtml += `
                    <div class="notification-item ${unreadClass}" data-notification-id="${notification.id}">
                        <div class="notification-content">
                            <p class="notification-message">${notification.message}</p>
                            <div class="notification-meta">
                                <span class="notification-category ${notification.category_key}">${notification.category}</span>
                                <span class="notification-time">${formatDate(notification.timestamp)}</span>
                            </div>
                        </div>
                        ${markReadButton}
                    </div>
                `;
            });
        } else {
            notificationsHtml = `
                <div class="no-notifications">
                    <p>No notifications</p>
                </div>
            `;
        }
        
        notificationsList.html(notificationsHtml);
        
        // Rebind event handlers for new elements
        container.find('.mark-read').on('click', function(e) {
            e.stopPropagation();
            const notificationItem = $(this).closest('.notification-item');
            const notificationId = notificationItem.data('notification-id');
            
            // Get WebSocket connection if available
            const ws = container.data('websocket');
            markNotificationAsRead(notificationId, notificationItem, container, ws);
        });
    }
    
    function formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})(django.jQuery);