from django.shortcuts import render
from rest_framework import viewsets
from .models import Room , Message
from .serializers import MessageSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class=RoomSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(users=self.request.user).prefetch_related('users')



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class=MessageSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = Message.objects.filter(room__users=self.request.user).select_related(
            'user', 'room').order_by('-created_at')
        room_id = self.request.query_params.get('room',None)
        if room_id :
            return queryset.filter(room_id=room_id)

        return queryset