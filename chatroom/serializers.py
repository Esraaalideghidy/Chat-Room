from rest_framework import serializers

from .models import Room,Message


class RoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id','users','name','created_at']

    def get_users(self,obj : Room):
        return [user.username for user in obj.users.all()]


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id','user','room','content','created_at']

    def get_user(self,obj : Message):
        return obj.user.username if obj.user else None
