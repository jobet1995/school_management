from django.core.management.base import BaseCommand
from cms_plugins.models import TestimonialPlugin, TestimonialItem

class Command(BaseCommand):
    help = 'Create sample testimonials for testing'

    def handle(self, *args, **options):
        # Create a testimonial plugin
        try:
            plugin = TestimonialPlugin()
            plugin.save()
            self.stdout.write(
                'Successfully created testimonial plugin'
            )
        except Exception as e:
            self.stdout.write(
                'Testimonial plugin may already exist or error occurred: %s' % str(e)
            )
            # Try to get existing plugin
            try:
                plugin = TestimonialPlugin.objects.first()
                if not plugin:
                    plugin = TestimonialPlugin()
                    plugin.save()
            except Exception:
                self.stdout.write(
                    'Failed to create or retrieve testimonial plugin'
                )
                return
        
        # Create sample testimonials
        testimonials_data = [
            {
                'name': 'Sarah Johnson',
                'course': 'Computer Science',
                'testimonial': 'This system has completely transformed how I manage my academic life. Everything is so intuitive and easy to use! The course materials are always up-to-date, and I can access everything from anywhere.',
                'is_featured': True
            },
            {
                'name': 'Michael Chen',
                'course': 'Business Administration',
                'testimonial': 'As a working professional pursuing my MBA, this platform has been a game-changer. The flexible scheduling and mobile access allow me to keep up with my studies while managing my career.',
                'is_featured': False
            },
            {
                'name': 'Emma Rodriguez',
                'course': 'Psychology',
                'testimonial': 'The interactive features and discussion forums have made learning so much more engaging. I feel more connected to my classmates and professors than I ever did in traditional classroom settings.',
                'is_featured': True
            },
            {
                'name': 'David Kim',
                'course': 'Engineering',
                'testimonial': 'The virtual labs and simulation tools are incredible. They provide hands-on experience that rivals physical labs, and I can repeat experiments as many times as I need to master the concepts.',
                'is_featured': False
            },
            {
                'name': 'Olivia Smith',
                'course': 'Art History',
                'testimonial': 'The multimedia resources and virtual museum tours have enriched my learning experience beyond what I thought possible in an online environment. The professors are truly dedicated to making art accessible to everyone.',
                'is_featured': False
            },
            {
                'name': 'James Wilson',
                'course': 'Medicine',
                'testimonial': 'The clinical case studies and peer collaboration features have been invaluable for my medical training. I can discuss complex cases with classmates from around the world and learn different perspectives.',
                'is_featured': True
            }
        ]

        for i, data in enumerate(testimonials_data):
            try:
                testimonial, created = TestimonialItem.objects.get_or_create(
                    testimonial_plugin=plugin,
                    name=data['name'],
                    defaults={
                        'course': data['course'],
                        'testimonial': data['testimonial'],
                        'is_featured': data['is_featured']
                    }
                )
                if created:
                    self.stdout.write(
                        'Successfully created testimonial: %s' % testimonial.name
                    )
                else:
                    self.stdout.write(
                        'Testimonial already exists: %s' % testimonial.name
                    )
            except Exception as e:
                self.stdout.write(
                    'Error creating testimonial %s: %s' % (data['name'], str(e))
                )