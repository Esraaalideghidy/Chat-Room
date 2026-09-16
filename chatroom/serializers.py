from rest_framework import serializers

from .models import Room,Message


class RoomSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')
    class Meta:
        model = Room
        fields = ['id','user_name','name','created_at']


class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Message
        fields = ['id','user_name','room','content','created_at']