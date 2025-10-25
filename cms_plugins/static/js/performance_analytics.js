(function($) {
    $(document).ready(function() {
        // Initialize all performance analytics plugins
        $('.performance-analytics').each(function() {
            initializePerformanceAnalytics($(this));
        });
    });

    function initializePerformanceAnalytics(container) {
        const pluginId = container.data('plugin-id');
        const timeRangeSelect = container.find('#time-range');
        const loadingSpinner = container.find('.loading-spinner');
        const errorMessage = container.find('.error-message');
        
        // Initialize charts
        let academicPerformanceChart = null;
        let attendanceRateChart = null;
        let activityTrendsChart = null;
        
        // Load initial data
        loadData(pluginId, timeRangeSelect.val(), container, loadingSpinner, errorMessage, 
                 (data) => {
                     academicPerformanceChart = createAcademicPerformanceChart(data.academic_performance);
                     attendanceRateChart = createAttendanceRateChart(data.attendance_rate);
                     activityTrendsChart = createActivityTrendsChart(data.activity_trends);
                 });
        
        // Handle time range change
        timeRangeSelect.on('change', function() {
            const selectedRange = $(this).val();
            loadData(pluginId, selectedRange, container, loadingSpinner, errorMessage,
                     (data) => {
                         updateAcademicPerformanceChart(academicPerformanceChart, data.academic_performance);
                         updateAttendanceRateChart(attendanceRateChart, data.attendance_rate);
                         updateActivityTrendsChart(activityTrendsChart, data.activity_trends);
                     });
        });
    }
    
    function loadData(pluginId, timeRange, container, loadingSpinner, errorMessage, onSuccess) {
        // Show loading spinner
        loadingSpinner.show();
        errorMessage.hide();
        container.find('.analytics-content').hide();
        
        // Make AJAX request to get chart data
        $.ajax({
            url: `/cms_plugins/performance-analytics/${pluginId}/`,
            method: 'GET',
            data: {
                'time_range': timeRange
            },
            success: function(response) {
                if (response.success) {
                    onSuccess(response.data);
                    container.find('.analytics-content').show();
                } else {
                    errorMessage.show();
                    console.error('Error loading analytics data:', response.error);
                }
            },
            error: function(xhr, status, error) {
                errorMessage.show();
                console.error('AJAX Error:', error);
            },
            complete: function() {
                // Hide loading spinner
                loadingSpinner.hide();
            }
        });
    }
    
    function createAcademicPerformanceChart(data) {
        const ctx = document.getElementById('academicPerformanceChart').getContext('2d');
        
        // Extract labels and data points
        const labels = data.map(item => formatDate(item.date));
        const grades = data.map(item => item.points);
        
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Academic Performance (Grade Points)',
                    data: grades,
                    borderColor: '#1E3A8A',
                    backgroundColor: 'rgba(30, 58, 138, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const index = context.dataIndex;
                                const item = data[index];
                                return `${context.dataset.label}: ${item.grade} (${context.parsed.y})`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 4.5,
                        ticks: {
                            stepSize: 0.5
                        },
                        title: {
                            display: true,
                            text: 'Grade Points'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
    
    function createAttendanceRateChart(data) {
        const ctx = document.getElementById('attendanceRateChart').getContext('2d');
        
        // Extract labels and data points
        const labels = data.map(item => formatDate(item.date));
        const rates = data.map(item => item.rate);
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Attendance Rate (%)',
                    data: rates,
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: '#10B981',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 10
                        },
                        title: {
                            display: true,
                            text: 'Attendance Rate (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
    
    function createActivityTrendsChart(data) {
        const ctx = document.getElementById('activityTrendsChart').getContext('2d');
        
        // Extract labels and data points
        const labels = data.map(item => formatDate(item.date));
        const activities = data.map(item => item.activities);
        
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Activities',
                    data: activities,
                    borderColor: '#F59E0B',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Activities'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
    
    function updateAcademicPerformanceChart(chart, data) {
        // Update labels and data
        chart.data.labels = data.map(item => formatDate(item.date));
        chart.data.datasets[0].data = data.map(item => item.points);
        chart.update();
    }
    
    function updateAttendanceRateChart(chart, data) {
        // Update labels and data
        chart.data.labels = data.map(item => formatDate(item.date));
        chart.data.datasets[0].data = data.map(item => item.rate);
        chart.update();
    }
    
    function updateActivityTrendsChart(chart, data) {
        // Update labels and data
        chart.data.labels = data.map(item => formatDate(item.date));
        chart.data.datasets[0].data = data.map(item => item.activities);
        chart.update();
    }
    
    function formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
        });
    }
})(django.jQuery);