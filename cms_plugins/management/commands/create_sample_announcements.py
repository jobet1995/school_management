from django.core.management.base import BaseCommand
from cms_plugins.models import Announcement

class Command(BaseCommand):
    help = 'Create sample announcements for testing'

    def handle(self, *args, **options):
        # Create sample announcements
        announcements_data = [
            {
                'title': 'University Closed for Holiday',
                'content': 'The university will be closed on November 1st for All Saints\' Day. All classes and administrative services will resume on November 2nd.',
                'is_published': True
            },
            {
                'title': 'New Library Hours',
                'content': 'Starting next week, the library will extend its opening hours during exam periods. Please check the updated schedule at the library entrance.',
                'is_published': True
            },
            {
                'title': 'Career Fair This Friday',
                'content': 'Join us for our annual career fair this Friday from 10am to 4pm in the Student Union Building. Over 50 companies will be attending, including major tech firms, financial institutions, and consulting companies. Don\'t miss this opportunity to network with potential employers and learn about internship and job opportunities. Bring your resumes and dress professionally.',
                'is_published': True
            },
            {
                'title': 'Campus WiFi Upgrade',
                'content': 'The campus WiFi network will be upgraded this weekend. There may be intermittent connectivity issues on Saturday and Sunday. We apologize for any inconvenience this may cause.',
                'is_published': True
            },
            {
                'title': 'New Student Support Services',
                'content': 'We are excited to announce the launch of new student support services including mental health counseling, academic tutoring, and career guidance. These services are available to all students at no additional cost.',
                'is_published': True
            }
        ]

        for data in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'is_published': data['is_published']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created announcement: {announcement.title}')
                )
            else:
                self.stdout.write(
                    f'Announcement already exists: {announcement.title}'
                )