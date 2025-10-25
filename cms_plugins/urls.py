from django.urls import path
from . import views

app_name = 'cms_plugins'

urlpatterns = [
    path('featured-announcements/<int:plugin_id>/', views.FeaturedAnnouncementsAjaxView.as_view(), name='featured_announcements_ajax'),
    path('featured-announcements/detail/<int:announcement_id>/', views.FeaturedAnnouncementDetailView.as_view(), name='featured_announcement_detail'),
    path('upcoming-events/<int:plugin_id>/', views.UpcomingEventsAjaxView.as_view(), name='upcoming_events_ajax'),
    path('course-search/', views.CourseSearchAjaxView.as_view(), name='course_search_ajax'),
    path('course-search-demo/', views.course_search_demo, name='course_search_demo'),
    path('statistics-counter-demo/', views.statistics_counter_demo, name='statistics_counter_demo'),
    path('cta-banner-demo/', views.cta_banner_demo, name='cta_banner_demo'),
    path('loading-spinner-demo/', views.loading_spinner_demo, name='loading_spinner_demo'),
]