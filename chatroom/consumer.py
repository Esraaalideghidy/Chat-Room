
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from chatroom.models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group,
            self.channel_name
        )

    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message =text_data_json['message']
        message_obj = await self.create_message(message)


        await self.channel_layer.group_send(
            self.room_group,
            {"type":'chat_message',
             "message":message}
        )

    async def chat_message(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({'message':message}))


    @database_sync_to_async
    def create_message(self, content):
        # user = self.scope["user"]
        user = User.objects.get(username="esraa")

        return Message.objects.create(
            user=user,
            room_id=self.room_id,
            content=content
        )
