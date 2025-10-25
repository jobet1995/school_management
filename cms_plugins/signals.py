from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import LiveNotification

@receiver(post_save, sender=LiveNotification)
def send_notification_via_websocket(sender, instance, created, **kwargs):
    """
    Send a notification via WebSocket when a new notification is created.
    """
    if created:
        try:
            channel_layer = get_channel_layer()
            if channel_layer is not None:
                group_name = f'notifications_{instance.user.id}'
                
                # Prepare notification data
                notification_data = {
                    'id': instance.id,
                    'message': instance.message,
                    'category': instance.get_category_display(),
                    'category_key': instance.category,
                    'is_read': instance.is_read,
                    'timestamp': instance.timestamp.isoformat(),
                }
                
                # Send notification to the user's group
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'send_notification_update',
                        'notification_data': notification_data
                    }
                )
        except Exception as e:
            # If WebSocket fails, that's okay - the notification is still in the database
            print(f"Failed to send WebSocket notification: {e}")