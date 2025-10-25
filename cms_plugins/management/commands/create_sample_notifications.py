from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cms_plugins.models import LiveNotification

class Command(BaseCommand):
    help = 'Create sample notifications for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of notifications to create per user (default: 5)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get all users
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(
                self.style.WARNING('No users found. Please create users first.')
            )
            return
        
        notification_count = 0
        
        # Create sample notifications for each user
        for user in users:
            for i in range(count):
                # Create different types of notifications
                if i % 4 == 0:
                    category = 'announcement'
                    message = f'New announcement posted: "Welcome to the new semester"'
                elif i % 4 == 1:
                    category = 'grade'
                    message = f'Your grade for {["Math 101", "English 101", "Science 101", "History 101"][i % 4]} has been released'
                elif i % 4 == 2:
                    category = 'event'
                    message = f'Reminder: {["Exam", "Project Due", "Class Meeting", "Field Trip"][i % 4]} tomorrow'
                else:
                    category = 'system'
                    message = f'System maintenance scheduled for tonight'
                
                # Create notification
                LiveNotification.objects.create(
                    user=user,
                    message=message,
                    category=category,
                    is_read=(i % 3 == 0)  # Mark some as read
                )
                notification_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {notification_count} sample notifications for {users.count()} users'
            )
        )