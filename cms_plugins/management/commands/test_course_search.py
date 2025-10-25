from django.core.management.base import BaseCommand
from django.test import RequestFactory
from cms_plugins.views import CourseSearchAjaxView
from cms_plugins.models import Course

class Command(BaseCommand):
    help = 'Test the course search functionality'

    def handle(self, *args, **options):
        # Create a request factory
        factory = RequestFactory()
        
        # Test search with a query that should return results
        request = factory.get('/cms_plugins/course-search/', {'q': 'computer'})
        view = CourseSearchAjaxView.as_view()
        response = view(request)
        
        # Print response
        self.stdout.write(
            self.style.SUCCESS(f'Response status code: {response.status_code}')
        )
        
        # Get response content
        content = response.content.decode()
        self.stdout.write(
            self.style.SUCCESS(f'Response content: {content}')
        )
        
        # Test with another query
        request = factory.get('/cms_plugins/course-search/', {'q': 'art'})
        response = view(request)
        
        # Print response
        self.stdout.write(
            self.style.SUCCESS(f'Response status code: {response.status_code}')
        )
        
        # Get response content
        content = response.content.decode()
        self.stdout.write(
            self.style.SUCCESS(f'Response content: {content}')
        )