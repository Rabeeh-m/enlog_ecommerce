import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger(__name__)

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        headers = {k.decode('utf-8'): v.decode('utf-8') for k, v in self.scope.get('headers', [])}
        auth_header = headers.get('authorization')
        logger.info(f"WebSocket connect - User: {self.user}, Headers: {headers}, Auth Header: {auth_header}")
        if self.user.is_authenticated:
            logger.info(f"Authenticated user ID: {self.user.id}")
            self.group_name = f'user_{self.user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            logger.error("Unauthenticated WebSocket connection attempt")
            await self.close(code=403)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def order_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))