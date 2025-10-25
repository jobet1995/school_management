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
    PerformanceAnalyticsPlugin,
    AttendanceTrackerPlugin,
    Attendance,
    Enrollment
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
                # Using union of separate queries to avoid type checking errors with Q objects
                courses_query = (courses_query.filter(title__icontains=query)
                             .union(courses_query.filter(code__icontains=query))
                             .union(courses_query.filter(description__icontains=query))
                             .union(courses_query.filter(instructor__icontains=query)))
            
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

class AttendanceTrackerUpdateView(View):
    """
    AJAX view to update student attendance records
    """
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, plugin_id):
        """
        Update attendance status for a specific student enrollment
        """
        try:
            # Get the plugin instance
            plugin = get_object_or_404(AttendanceTrackerPlugin, id=plugin_id)
            
            # Get parameters from POST data
            enrollment_id = request.POST.get('enrollment_id')
            status = request.POST.get('status')  # 'present' or 'absent'
            search_query = request.POST.get('search_query', '')
            
            # Validate enrollment_id
            if not enrollment_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Enrollment ID is required'
                }, status=400)
            
            # Validate status
            if status not in ['present', 'absent']:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status value'
                }, status=400)
            
            # Get the enrollment
            enrollment = get_object_or_404(Enrollment, id=enrollment_id, is_active=True)
            
            # Determine if student is present
            is_present = (status == 'present')
            
            # Get or create attendance record for this student, course, and date
            attendance, created = Attendance.objects.get_or_create(
                student=enrollment.student,
                course=enrollment.course,
                date=plugin.date,
                defaults={
                    'is_present': is_present,
                    'is_excused': False
                }
            )
            
            # If record already existed, update it
            if not created:
                attendance.is_present = is_present
                attendance.save()
            
            # Get updated attendance data
            attendance_data = plugin.get_attendance_data(search_query)
            
            # Return JSON response with updated data
            return JsonResponse({
                'success': True,
                'message': f'Attendance updated successfully',
                'attendance_data': attendance_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

class StudyRecommendationsAjaxView(View):
    """
    AJAX view to fetch study recommendations with filtering capabilities
    """
    
    def get(self, request, plugin_id):
        """
        Return study recommendations for a specific plugin instance with optional filtering
        """
        try:
            # Import here to avoid circular imports
            from .models import StudyRecommendationPlugin, Student
            
            # Get the plugin instance
            plugin = get_object_or_404(StudyRecommendationPlugin, id=plugin_id)
            
            # Get filter parameters
            difficulty_filter = request.GET.get('difficulty', '')
            subject_filter = request.GET.get('subject', '')
            
            # In a real implementation, you would get the student from the authenticated user
            # For now, we'll demonstrate with a sample student or None
            student = None
            student_id = request.GET.get('student_id')
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                except Student.DoesNotExist:  # type: ignore
                    pass
            
            # Get recommendations with filtering
            recommendations_data = plugin.get_recommendations(
                student=student,
                difficulty_filter=difficulty_filter,
                subject_filter=subject_filter
            )
            
            # Get filter choices
            subject_choices = plugin.get_subject_choices()
            difficulty_choices = plugin.get_difficulty_choices()
            
            # Return JSON response
            return JsonResponse({
                'success': True,
                'recommendations': recommendations_data,
                'title': plugin.title,
                'filters': {
                    'subjects': [{'value': choice[0], 'label': choice[1]} for choice in subject_choices],
                    'difficulties': [{'value': choice[0], 'label': choice[1]} for choice in difficulty_choices],
                    'current_difficulty': difficulty_filter,
                    'current_subject': subject_filter
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
