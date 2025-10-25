from django.core.management.base import BaseCommand
from django.utils import timezone
from cms_plugins.models import Event
import random

class Command(BaseCommand):
    help = 'Create sample events for testing'

    def handle(self, *args, **options):
        # Create sample events
        events_data = [
            {
                'title': 'University Graduation Ceremony',
                'description': 'Annual graduation ceremony for all graduating students. Celebrate the achievements of our students with family and friends.',
                'start_date': timezone.now() + timezone.timedelta(days=30),
                'end_date': timezone.now() + timezone.timedelta(days=30, hours=3),
                'location': 'Main Auditorium',
                'category': 'academic',
                'is_published': True
            },
            {
                'title': 'Football Championship',
                'description': 'Exciting football championship match between our university team and the regional champions. Come support our team!',
                'start_date': timezone.now() + timezone.timedelta(days=10),
                'end_date': timezone.now() + timezone.timedelta(days=10, hours=2),
                'location': 'University Stadium',
                'category': 'sports',
                'is_published': True
            },
            {
                'title': 'Art Exhibition Opening',
                'description': 'Opening of the annual student art exhibition featuring works from our talented art students across all disciplines.',
                'start_date': timezone.now() + timezone.timedelta(days=5),
                'end_date': timezone.now() + timezone.timedelta(days=20),
                'location': 'Art Gallery',
                'category': 'cultural',
                'is_published': True
            },
            {
                'title': 'Student Social Mixer',
                'description': 'Join us for a fun evening of food, music, and socializing with fellow students from all faculties.',
                'start_date': timezone.now() + timezone.timedelta(days=15),
                'end_date': timezone.now() + timezone.timedelta(days=15, hours=4),
                'location': 'Student Union Building',
                'category': 'social',
                'is_published': True
            },
            {
                'title': 'Administrative Office Closure',
                'description': 'University administrative offices will be closed for annual maintenance and system upgrades.',
                'start_date': timezone.now() + timezone.timedelta(days=25),
                'end_date': timezone.now() + timezone.timedelta(days=27),
                'location': 'All Administrative Buildings',
                'category': 'administrative',
                'is_published': True
            },
            {
                'title': 'Research Symposium',
                'description': 'Annual research symposium showcasing the latest findings from our faculty and graduate students across all departments.',
                'start_date': timezone.now() + timezone.timedelta(days=45),
                'end_date': timezone.now() + timezone.timedelta(days=45, hours=6),
                'location': 'Conference Center',
                'category': 'academic',
                'is_published': True
            },
            {
                'title': 'Basketball Tournament',
                'description': 'Weekend basketball tournament featuring teams from various universities in the region.',
                'start_date': timezone.now() + timezone.timedelta(days=12),
                'end_date': timezone.now() + timezone.timedelta(days=14),
                'location': 'University Gymnasium',
                'category': 'sports',
                'is_published': True
            }
        ]

        categories = ['academic', 'sports', 'cultural', 'social', 'administrative']
        
        for data in events_data:
            event, created = Event.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'start_date': data['start_date'],
                    'end_date': data['end_date'],
                    'location': data['location'],
                    'category': data['category'],
                    'is_published': data['is_published']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created event: %s' % event.title)
                )
            else:
                self.stdout.write(
                    'Event already exists: %s' % event.title
                )

        # Create some additional random events
        for i in range(5):
            category = random.choice(categories)
            event_data = {
                'title': '%s Event %s' % (category.capitalize(), i+1),
                'description': 'This is a sample %s event for testing purposes.' % category,
                'start_date': timezone.now() + timezone.timedelta(days=random.randint(1, 60)),
                'end_date': timezone.now() + timezone.timedelta(days=random.randint(1, 60) + random.randint(1, 5)),
                'location': 'Location %s' % (i+1),
                'category': category,
                'is_published': True
            }
            
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created event: %s' % event.title)
                )