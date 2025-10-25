(function($) {
    $(document).ready(function() {
        // Initialize all student dashboard plugins
        $('.student-dashboard').each(function() {
            initializeStudentDashboard($(this));
        });
    });

    function initializeStudentDashboard(dashboard) {
        const pluginId = dashboard.data('plugin-id');
        const refreshBtn = dashboard.find('.refresh-btn');
        const loadingSpinner = dashboard.find('.loading-spinner');
        
        // Set initial progress bar widths
        updateProgressBars(dashboard);
        
        // Handle refresh button click
        refreshBtn.on('click', function() {
            refreshDashboard(pluginId, dashboard, loadingSpinner);
        });
    }
    
    function refreshDashboard(pluginId, dashboard, loadingSpinner) {
        // Show loading spinner
        loadingSpinner.show();
        
        // Make AJAX request
        $.ajax({
            url: `/cms_plugins/student-dashboard/${pluginId}/`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    updateDashboardContent(dashboard, response.data);
                } else {
                    console.error('Error refreshing dashboard:', response.error);
                    showError(dashboard, 'Failed to refresh dashboard. Please try again.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
                showError(dashboard, 'Failed to refresh dashboard. Please try again.');
            },
            complete: function() {
                // Hide loading spinner
                loadingSpinner.hide();
                
                // Update progress bars with animation
                updateProgressBars(dashboard);
            }
        });
    }
    
    function updateDashboardContent(dashboard, data) {
        // Update student info
        const studentInfo = dashboard.find('.student-info .student-details');
        if (studentInfo.length) {
            if (data.student && data.student.name) {
                studentInfo.html(`
                    <p><strong>Name:</strong> ${data.student.name}</p>
                    <p><strong>Student ID:</strong> ${data.student.student_id}</p>
                    <p><strong>Email:</strong> ${data.student.email}</p>
                `);
            } else {
                studentInfo.html('<p>Please log in to view your dashboard.</p>');
            }
        }
        
        // Update overall attendance
        const attendanceSummary = dashboard.find('.attendance-summary');
        if (attendanceSummary.length && data.attendance_percentage !== undefined) {
            attendanceSummary.find('.percentage').text(`${data.attendance_percentage}%`);
            attendanceSummary.find('.attendance-bar').data('percentage', data.attendance_percentage);
        }
        
        // Update enrolled courses
        const coursesGrid = dashboard.find('.courses-grid');
        if (coursesGrid.length && data.enrolled_courses) {
            if (data.enrolled_courses.length > 0) {
                let coursesHtml = '';
                data.enrolled_courses.forEach(course => {
                    coursesHtml += `
                        <div class="dashboard-card course-card" data-course-id="${course.id}">
                            <h4>${course.code} - ${course.title}</h4>
                            <p class="instructor">Instructor: ${course.instructor}</p>
                            <div class="progress-container" data-progress="${course.progress}">
                                <span>Progress: ${course.progress}%</span>
                                <div class="progress-bar">
                                    <div class="progress-fill"></div>
                                </div>
                            </div>
                            <div class="attendance-container" data-attendance="${course.attendance}">
                                <span>Attendance: ${course.attendance}%</span>
                                <div class="attendance-bar">
                                    <div class="attendance-fill"></div>
                                </div>
                            </div>
                        </div>
                    `;
                });
                coursesGrid.html(coursesHtml);
            } else {
                coursesGrid.html('<p>No courses enrolled.</p>');
            }
        }
        
        // Update recent grades
        const gradesList = dashboard.find('.grades-list');
        if (gradesList.length && data.recent_grades) {
            if (data.recent_grades.length > 0) {
                let gradesHtml = '';
                data.recent_grades.forEach(grade => {
                    gradesHtml += `
                        <div class="dashboard-card grade-item">
                            <div class="grade-header">
                                <h4>${grade.course_code} - ${grade.course}</h4>
                                <span class="grade-badge grade-${grade.grade}">${grade.grade}</span>
                            </div>
                            <p class="grade-date">Recorded: ${grade.date}</p>
                        </div>
                    `;
                });
                gradesList.html(gradesHtml);
            } else {
                gradesList.html('<p>No grades available.</p>');
            }
        }
    }
    
    function updateProgressBars(dashboard) {
        // Update overall attendance bar
        dashboard.find('.attendance-bar').each(function() {
            const percentage = $(this).data('percentage') || 0;
            $(this).find('.attendance-fill').css('width', `${percentage}%`);
        });
        
        // Update course progress bars
        dashboard.find('.progress-container').each(function() {
            const progress = $(this).data('progress') || 0;
            $(this).find('.progress-fill').css('width', `${progress}%`);
        });
        
        // Update course attendance bars
        dashboard.find('.attendance-container').each(function() {
            const attendance = $(this).data('attendance') || 0;
            $(this).find('.attendance-fill').css('width', `${attendance}%`);
        });
    }
    
    function showError(dashboard, message) {
        // In a real implementation, you might want to show an error message to the user
        console.error(message);
        // You could also add a visual error indicator to the dashboard
    }
})(django.jQuery);