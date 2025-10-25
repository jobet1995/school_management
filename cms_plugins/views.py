from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.utils import dateformat
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import (
    Announcement, 
    Event, 
    Course, 
    FeaturedAnnouncementsPlugin, 
    UpcomingEventsPlugin,
    StatisticsCounterPlugin,
    StatisticsCounterItem,
    StudentDashboardPlugin,
    LiveNotification,
    LiveNotificationsPlugin,
    PerformanceAnalyticsPlugin
)

# Create your views here.

class PerformanceAnalyticsAjaxView(View):
    """
    AJAX view to fetch performance analytics data
    """
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, plugin_id):
        """
        Return performance analytics data for a specific plugin instance
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(PerformanceAnalyticsPlugin, id=plugin_id)
            
            # Get time range from query parameters
            time_range = request.GET.get('time_range', plugin.default_time_range)
            
            # Get chart data for the current user
            chart_data = plugin.get_chart_data(request.user, time_range)
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'data': chart_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class LiveNotificationsAjaxView(View):
    """
    AJAX view to fetch live notifications data
    """
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, plugin_id):
        """
        Return notifications data for a specific plugin instance
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(LiveNotificationsPlugin, id=plugin_id)
            
            # Get notifications for the current user
            notifications = plugin.get_notifications(request.user)
            unread_count = plugin.get_unread_count(request.user)
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'notifications': notifications,
                'unread_count': unread_count
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class MarkNotificationAsReadView(View):
    """
    AJAX view to mark a notification as read
    """
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, notification_id):
        """
        Mark a specific notification as read
        """
        try:
            # Get the notification
            notification = get_object_or_404(LiveNotification, id=notification_id, user=request.user)
            
            # Mark as read
            notification.mark_as_read()
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'message': 'Notification marked as read'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class StudentDashboardAjaxView(View):
    """
    AJAX view to fetch student dashboard data
    """
    
    def get(self, request, plugin_id):
        """
        Return student dashboard data for a specific plugin instance
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(StudentDashboardPlugin, id=plugin_id)
            
            # Get student ID from session or request (simplified for demo)
            # In a real implementation, you would get this from the authenticated user
            student_id = request.GET.get('student_id', None)
            
            # Get student data
            student_data = plugin.get_student_data(student_id)
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'data': student_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class FeaturedAnnouncementsAjaxView(View):
    """
    AJAX view to fetch featured announcements data
    """
    
    def get(self, request, plugin_id):
        """
        Return announcements data for a specific plugin instance
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(FeaturedAnnouncementsPlugin, id=plugin_id)
            
            # Get announcements data
            announcements_data = plugin.get_announcements_data()
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'announcements': announcements_data,
                'title': plugin.title
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class FeaturedAnnouncementDetailView(View):
    """
    AJAX view to fetch full announcement content
    """
    
    def get(self, request, announcement_id):
        """
        Return full announcement content for a specific announcement
        """
        try:
            # Import here to avoid circular imports
            from .models import Announcement
            
            # Get the announcement
            announcement = get_object_or_404(Announcement, id=announcement_id, is_published=True)
            
            # Return JSON response with full content
            return JsonResponse({
                'success': True,
                'announcement': {
                    'id': announcement.id,
                    'title': announcement.title,
                    'content': announcement.content,
                    'created_at': announcement.created_at.isoformat()
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class UpcomingEventsAjaxView(View):
    """
    AJAX view to fetch upcoming events data with filtering capabilities
    """
    
    def get(self, request, plugin_id):
        """
        Return events data for a specific plugin instance with optional filtering
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(UpcomingEventsPlugin, id=plugin_id)
            
            # Get filter parameters
            category = request.GET.get('category', '')
            date_filter = request.GET.get('date_filter', '')
            
            # Get events data with filtering
            events_data = plugin.get_events_data(category, date_filter)
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'events': events_data,
                'title': plugin.title,
                'enable_carousel': plugin.enable_carousel,
                'auto_rotate': plugin.auto_rotate,
                'rotation_interval': plugin.rotation_interval
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class CourseSearchAjaxView(View):
    """
    AJAX view to search courses dynamically
    """
    
    def get(self, request):
        """
        Return courses matching the search query
        """
        try:
            # Get search query
            query = request.GET.get('q', '').strip()
            
            # Base query for published courses
            courses_query = Course.objects.filter(is_published=True)
            
            # Apply search filter if query exists
            if query:
                courses_query = courses_query.filter(
                    Q(title__icontains=query) | 
                    Q(code__icontains=query) | 
                    Q(description__icontains=query) | 
                    Q(instructor__icontains=query)
                )
            
            # Limit results to 10
            courses = list(courses_query[:10])
            
            # Format data for JSON response
            courses_data = []
            for course in courses:
                courses_data.append({
                    'id': course.id,
                    'title': course.title,
                    'code': course.code,
                    'description': course.description,
                    'instructor': course.instructor,
                    'category': course.get_category_display(),
                    'category_key': course.category,
                    'credits': course.credits,
                })
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'courses': courses_data,
                'query': query,
                'count': len(courses_data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)