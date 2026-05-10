from django.db import models
from django.contrib.auth.models import User

class chatroom(models.Model):
    room_name= models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
# Create your models here.
class Message(models.Model):
    chatroom_name= models.ForeignKey(chatroom, on_delete=models.PROTECT)
    user_name = models.ForeignKey(User,on_delete=models.CASCADE, related_name="messagesb" )
    message= models.TextField()
    reaction= models.TextChoices
    timestamp = models.DateTimeField(auto_now_add=True)

