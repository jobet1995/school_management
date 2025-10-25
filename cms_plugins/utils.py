from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import LiveNotification

def send_notification_to_user(user, message, category='system'):
    """
    Create a notification for a user and send it via WebSocket if the user is connected.
    """
    # Create the notification in the database
    notification = LiveNotification.objects.create(
        user=user,
        message=message,
        category=category
    )
    
    # Try to send via WebSocket
    try:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            group_name = f'notifications_{user.id}'
            
            # Prepare notification data
            notification_data = {
                'id': notification.id,
                'message': notification.message,
                'category': notification.get_category_display(),
                'category_key': notification.category,
                'is_read': notification.is_read,
                'timestamp': notification.timestamp.isoformat(),
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
    
    return notification