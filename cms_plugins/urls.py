from django.urls import path
from . import views

app_name = 'cms_plugins'

urlpatterns = [
    path('performance-analytics/<int:plugin_id>/', views.PerformanceAnalyticsAjaxView.as_view(), name='performance_analytics_ajax'),
    path('live-notifications/<int:plugin_id>/', views.LiveNotificationsAjaxView.as_view(), name='live_notifications_ajax'),
    path('mark-notification-as-read/<int:notification_id>/', views.MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
    path('student-dashboard/<int:plugin_id>/', views.StudentDashboardAjaxView.as_view(), name='student_dashboard_ajax'),
    path('featured-announcements/<int:plugin_id>/', views.FeaturedAnnouncementsAjaxView.as_view(), name='featured_announcements_ajax'),
    path('featured-announcements/detail/<int:announcement_id>/', views.FeaturedAnnouncementDetailView.as_view(), name='featured_announcement_detail'),
    path('upcoming-events/<int:plugin_id>/', views.UpcomingEventsAjaxView.as_view(), name='upcoming_events_ajax'),
    path('course-search/', views.CourseSearchAjaxView.as_view(), name='course_search_ajax'),
]