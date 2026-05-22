from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_name= models.CharField(null=False, max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    HAPPY = '😄'
    EVIL = '😈'
    RAGE = '😡'
    TABLEV = '🤬'
    SHRUGGING = '🤷'
    CUTE = '🥰'
    SIGMA = '😎'
    FIGHT = '💪'
    SUS = '🤨'
    EXHAUSTED = '😮‍💨'
    EXTRA = '✨'
    CONFUSED = '😵'
    NONE = ''

    REACTION_CHOICES = (
        (CONFUSED, '😵 Confused'),
        (HAPPY, '😄 Happy'),
        (EVIL, '😈 Evil'),
        (RAGE, '😡 Rage'),
        (TABLEV, '🤬 Table Flip'),
        (SHRUGGING, '🤷 Shrugging'),
        (CUTE, '🥰 Cute'),
        (SIGMA, '😎 Sigma'),
        (FIGHT, '💪 Fight'),
        (SUS, '🤨 Sus'),
        (EXHAUSTED, '😮‍💨 Exhausted'),
        (EXTRA, '✨ Extra'),
        (NONE, 'No Reaction')
    )
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author_message" )
    message= models.TextField()
    reaction= models.CharField(max_length = 50,choices=REACTION_CHOICES, default=NONE)
    timestamp = models.DateTimeField(auto_now_add=True)
    room= models.ForeignKey(Room, on_delete=models.CASCADE)


    def __str__(self):
        return self.author.username
    
    @classmethod
    def last__messages(cls):
        return Message.objects.order_by('-timestamp').all()
