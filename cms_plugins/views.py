from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import FeaturedAnnouncementsPlugin, UpcomingEventsPlugin, Course, StatisticsCounterPlugin, StatisticsCounterItem

# Create your views here.

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

def course_search_demo(request):
    """
    Demo view for course search functionality
    """
    return render(request, 'course_search.html')

def statistics_counter_demo(request):
    """
    Demo view for statistics counter functionality
    """
    # Get the first statistics counter plugin
    plugin = StatisticsCounterPlugin.objects.first()
    if not plugin:
        # Create a demo plugin if none exists
        plugin = StatisticsCounterPlugin()
        plugin.save()
        
        # Create sample counters
        sample_counters = [
            {'label': 'Students', 'value': 5000, 'icon': 'fa fa-users'},
            {'label': 'Faculty', 'value': 300, 'icon': 'fa fa-graduation-cap'},
            {'label': 'Courses', 'value': 200, 'icon': 'fa fa-book'},
            {'label': 'Graduation Rate', 'value': 95, 'icon': 'fa fa-trophy'},
        ]
        
        for counter_data in sample_counters:
            counter = StatisticsCounterItem(
                statistics_counter_plugin=plugin,
                label=counter_data['label'],
                value=counter_data['value'],
                icon=counter_data['icon']
            )
            counter.save()
    
    counters = StatisticsCounterItem.objects.filter(statistics_counter_plugin=plugin)
    return render(request, 'statistics_counter_demo.html', {'counters': counters})

def cta_banner_demo(request):
    """
    Demo view for CTA banner functionality
    """
    return render(request, 'cta_banner_demo.html')

def loading_spinner_demo(request):
    """
    Demo view for loading spinner functionality
    """
    return render(request, 'loading_spinner_demo.html')
