from django.urls import path,include
from rest_framework.routers import DefaultRouter

from chatroom.views import MessageViewSet, RoomViewSet
router = DefaultRouter()

router.register(r'rooms',RoomViewSet,basename='chat_room')
router.register(r'Messages',MessageViewSet,basename='chat_message')

urlpatterns = [
    path('chat/',include(router.urls)),
]
