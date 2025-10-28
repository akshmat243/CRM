# home/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    print("Consumerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    async def connect(self):
        # Join the notifications group
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the notifications group
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )

    # Receive message from group
    async def send_notification(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
