from django.shortcuts import render
from rest_framework import viewsets
from .models import Room , Message
from .serializers import MessageSerializer, RoomSerializer
# Create your views here.


class RoomViewSet(viewsets.ModelViewSet):
    queryset= Room.objects.select_related('user')
    serializer_class=RoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related(
        'user', 'room').order_by('-created_at')
    serializer_class=MessageSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room',None)
        if room_id :
            return self.queryset.filter(room_id=room_id)

        return self.queryset