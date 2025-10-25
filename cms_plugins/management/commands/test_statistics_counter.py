from django.core.management.base import BaseCommand
from django.test import RequestFactory
from cms_plugins.views import statistics_counter_demo

class Command(BaseCommand):
    help = 'Test the statistics counter functionality'

    def handle(self, *args, **options):
        # Create a request factory
        factory = RequestFactory()
        
        # Test the statistics counter demo view
        request = factory.get('/cms_plugins/statistics-counter-demo/')
        response = statistics_counter_demo(request)
        
        self.stdout.write(
            self.style.SUCCESS(f'Response status code: {response.status_code}')
        )
        
        # Get response content
        content = response.content.decode()
        self.stdout.write(
            self.style.SUCCESS(f'Response content length: {len(content)}')
        )
        
        # Check if the response contains expected elements
        if 'statistics-counter-container' in content:
            self.stdout.write(
                self.style.SUCCESS('SUCCESS: Found statistics counter container in response')
            )
        else:
            self.stdout.write(
                'ERROR: Statistics counter container not found in response'
            )
        
        if 'statistics-counter-item' in content:
            self.stdout.write(
                self.style.SUCCESS('SUCCESS: Found statistics counter items in response')
            )
        else:
            self.stdout.write(
                'ERROR: Statistics counter items not found in response'
            )