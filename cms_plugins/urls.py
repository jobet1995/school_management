from django.urls import path
from . import views

app_name = 'cms_plugins'

urlpatterns = [
    path('featured-announcements/<int:plugin_id>/', views.FeaturedAnnouncementsAjaxView.as_view(), name='featured_announcements_ajax'),
    path('featured-announcements/detail/<int:announcement_id>/', views.FeaturedAnnouncementDetailView.as_view(), name='featured_announcement_detail'),
    path('upcoming-events/<int:plugin_id>/', views.UpcomingEventsAjaxView.as_view(), name='upcoming_events_ajax'),
    path('course-search/', views.CourseSearchAjaxView.as_view(), name='course_search_ajax'),
]