from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone



# Create your models here.


class Room(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True,editable=False)
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100 , unique = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
class Message(models.Model):
    id = models.UUIDField(default = uuid.uuid4 , primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete= models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.content} to {self.user}"
