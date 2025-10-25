import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import LiveNotification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Safely access url_route
        if 'url_route' in self.scope and 'kwargs' in self.scope['url_route']:
            self.user_id = self.scope['url_route']['kwargs'].get('user_id')
            self.room_group_name = f'notifications_{self.user_id}'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to room group
            if hasattr(self, 'room_group_name'):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'notification_message',
                        'message': message
                    }
                )

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Method to send notification to connected user
    async def send_notification_update(self, event):
        """
        Send a notification update to the WebSocket
        """
        notification_data = event['notification_data']
        
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification_update',
            'data': notification_data
        }))