
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from chatroom.models import Message, Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        ##check the user autentication
        if self.scope['user'].is_anonymous:
            await self.close()
            return
            
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = f'chat_{self.room_id}'
        ##check users member the room or not
        if not await self.is_room_member():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self,code):
        if hasattr(self, "room_group"):
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
        user = self.scope["user"]

        return Message.objects.create(
            user=user,
            room_id=self.room_id,
            content=content
        )

    @database_sync_to_async
    def is_room_member(self):
        return Room.objects.filter(id=self.room_id, users=self.scope['user']).exists()

