from django.urls import path

from chatroom.consumer import ChatConsumer

websocket_urlpatterns = [
    path(r'ws/chat/<uuid:room_id>/', ChatConsumer.as_asgi()),
]
