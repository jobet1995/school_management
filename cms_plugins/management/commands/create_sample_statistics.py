from django.core.management.base import BaseCommand
from cms_plugins.models import StatisticsCounterPlugin, StatisticsCounterItem

class Command(BaseCommand):
    help = 'Create sample statistics counters for testing'

    def handle(self, *args, **options):
        # Create a statistics counter plugin
        try:
            plugin = StatisticsCounterPlugin()
            plugin.save()
            self.stdout.write(
                'Successfully created statistics counter plugin'
            )
        except Exception as e:
            self.stdout.write(
                'Statistics counter plugin may already exist or error occurred: %s' % str(e)
            )
            # Try to get existing plugin
            try:
                plugin = StatisticsCounterPlugin.objects.first()
                if not plugin:
                    plugin = StatisticsCounterPlugin()
                    plugin.save()
            except Exception:
                self.stdout.write(
                    'Failed to create or retrieve statistics counter plugin'
                )
                return
        
        # Create sample counter items
        counters_data = [
            {
                'label': 'Students',
                'value': 5000,
                'icon': 'fa fa-users'
            },
            {
                'label': 'Faculty',
                'value': 300,
                'icon': 'fa fa-graduation-cap'
            },
            {
                'label': 'Courses',
                'value': 200,
                'icon': 'fa fa-book'
            },
            {
                'label': 'Graduation Rate',
                'value': 95,
                'icon': 'fa fa-trophy'
            }
        ]

        for i, data in enumerate(counters_data):
            try:
                counter, created = StatisticsCounterItem.objects.get_or_create(
                    statistics_counter_plugin=plugin,
                    label=data['label'],
                    defaults={
                        'value': data['value'],
                        'icon': data['icon']
                    }
                )
                if created:
                    self.stdout.write(
                        'Successfully created counter: %s' % counter.label
                    )
                else:
                    self.stdout.write(
                        'Counter already exists: %s' % counter.label
                    )
            except Exception as e:
                self.stdout.write(
                    'Error creating counter %s: %s' % (data['label'], str(e))
                )