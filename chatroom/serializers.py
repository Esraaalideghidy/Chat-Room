from rest_framework import serializers

from .models import Room,Message


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id','user','name','created_at']

    def get_user(self,obj : Room):
        return obj.user.username if obj.user else None


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id','user','room','content','created_at']

    def get_user(self,obj : Room):
        return obj.user.username if obj.user else None
