(function($) {
    $(document).ready(function() {
        // Initialize all attendance tracker plugins
        $('.attendance-tracker').each(function() {
            initializeAttendanceTracker($(this));
        });
    });

    function initializeAttendanceTracker(container) {
        const pluginId = container.data('plugin-id');
        const searchInput = container.find('#attendance-search');
        const searchBtn = container.find('#search-btn');
        const tableBody = container.find('#attendance-table-body');
        const loadingSpinner = container.find('.loading-spinner');
        const successNotification = container.find('#success-notification');
        const errorNotification = container.find('#error-notification');
        
        // Handle search button click
        searchBtn.on('click', function() {
            const searchQuery = searchInput.val().trim();
            searchAttendance(pluginId, searchQuery, container, loadingSpinner, tableBody);
        });
        
        // Handle Enter key in search input
        searchInput.on('keypress', function(e) {
            if (e.which === 13) { // Enter key
                searchBtn.click();
            }
        });
        
        // Handle attendance toggle buttons
        container.on('click', '.btn-toggle-attendance', function() {
            const button = $(this);
            const enrollmentId = button.data('enrollment');
            const currentStatus = button.data('status');
            const newStatus = currentStatus === 'present' ? 'absent' : 'present';
            
            updateAttendance(pluginId, enrollmentId, newStatus, container, loadingSpinner, successNotification, errorNotification);
        });
        
        // Handle notification close buttons
        container.on('click', '.notification-close', function() {
            $(this).closest('.notification').hide();
        });
    }
    
    function searchAttendance(pluginId, searchQuery, container, loadingSpinner, tableBody) {
        // Show loading spinner
        loadingSpinner.show();
        
        // Make AJAX request to get filtered attendance data
        $.ajax({
            url: `/cms_plugins/attendance-tracker/${pluginId}/update/`,
            method: 'POST',
            data: {
                'search_query': searchQuery
            },
            success: function(response) {
                if (response.success) {
                    updateAttendanceTable(tableBody, response.attendance_data.attendance_data);
                    updateSummary(container, response.attendance_data);
                } else {
                    showError(container, response.error || 'Failed to search attendance records.');
                }
            },
            error: function(xhr, status, error) {
                showError(container, 'Failed to search attendance records. Please try again.');
            },
            complete: function() {
                // Hide loading spinner
                loadingSpinner.hide();
            }
        });
    }
    
    function updateAttendance(pluginId, enrollmentId, newStatus, container, loadingSpinner, successNotification, errorNotification) {
        // Show loading spinner
        loadingSpinner.show();
        
        // Make AJAX request to update attendance
        $.ajax({
            url: `/cms_plugins/attendance-tracker/${pluginId}/update/`,
            method: 'POST',
            data: {
                'enrollment_id': enrollmentId,
                'status': newStatus
            },
            success: function(response) {
                if (response.success) {
                    // Update the UI with the new data
                    const tableBody = container.find('#attendance-table-body');
                    updateAttendanceTable(tableBody, response.attendance_data.attendance_data);
                    updateSummary(container, response.attendance_data);
                    
                    // Show success notification
                    showNotification(successNotification, response.message);
                } else {
                    showError(container, response.error || 'Failed to update attendance.');
                }
            },
            error: function(xhr, status, error) {
                showError(container, 'Failed to update attendance. Please try again.');
            },
            complete: function() {
                // Hide loading spinner
                loadingSpinner.hide();
            }
        });
    }
    
    function updateAttendanceTable(tableBody, attendanceData) {
        // Clear existing table rows
        tableBody.empty();
        
        // Add new rows
        attendanceData.forEach(function(item) {
            const row = `
                <tr data-enrollment-id="${item.enrollment_id}" data-attendance-id="${item.attendance_id || ''}">
                    <td>${item.student_name}</td>
                    <td>${item.course_code} - ${item.course_name}</td>
                    <td class="status-cell">
                        <span class="status-badge ${item.is_present ? 'present' : 'absent'}">
                            ${item.is_present ? 'Present' : 'Absent'}
                        </span>
                        ${item.is_excused ? '<span class="excused-badge">Excused</span>' : ''}
                    </td>
                    <td class="action-cell">
                        <button class="btn-toggle-attendance ${item.is_present ? 'present' : 'absent'}" 
                                data-enrollment="${item.enrollment_id}"
                                data-status="${item.is_present ? 'present' : 'absent'}">
                            ${item.is_present ? 'Mark Absent' : 'Mark Present'}
                        </button>
                    </td>
                </tr>
            `;
            tableBody.append(row);
        });
    }
    
    function updateSummary(container, attendanceData) {
        container.find('#completion-percentage').text(attendanceData.completion_percentage + '%');
        container.find('.progress-fill').css('width', attendanceData.completion_percentage + '%');
        container.find('#total-students').text(attendanceData.total_students);
        container.find('#marked-present').text(attendanceData.marked_present);
    }
    
    function showNotification(notificationElement, message) {
        notificationElement.find('.notification-message').text(message);
        notificationElement.show();
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            notificationElement.fadeOut();
        }, 5000);
    }
    
    function showError(container, message) {
        const errorNotification = container.find('#error-notification');
        showNotification(errorNotification, message);
    }
})(django.jQuery);