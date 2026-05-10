from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    CONFUSED = '(◎_◎;)'
    HAPPY = 'ヽ(•‿•)ノ'
    EVIL = 'ψ(｀∇´)ψ'
    RAGE = '(ノಠ益ಠ)ノ彡┻━┻'
    TABLEV = '(╯°□°）╯︵ ┻━┻'
    SHRUGGING = '┐(´д`)┌'
    CUTE = '(づ｡◕‿‿◕｡)づ'
    SIGMA = '(⌐■_■)'
    FIGHT = 'ᕦ(ò_óˇ)ᕤ'
    SUS = '(눈_눈)'
    EXHAUSTED = '(-_-)'
    EXTRA = '༼ つ ◕_◕ ༽つ'
    NONE = ''
    
    REACTION_CHOICES = (
    (CONFUSED, '(◎_◎;)'),
    (HAPPY, 'ヽ(•‿•)ノ'),
    (EVIL, 'ψ(｀∇´)ψ'),
    (RAGE, '(ノಠ益ಠ)ノ彡┻━┻'),
    (TABLEV, '(╯°□°）╯︵ ┻━┻'),
    (SHRUGGING, '┐(´д`)┌'),
    (CUTE, '(づ｡◕‿‿◕｡)づ'),
    (SIGMA, '(⌐■_■)'),
    (FIGHT, 'ᕦ(ò_óˇ)ᕤ'),
    (SUS, '(눈_눈)'),
    (EXHAUSTED, '(-_-)'),
    (EXTRA, '༼ つ ◕_◕ ༽つ'),
    (NONE, 'No Reaction')
    )

    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author_message" )
    message= models.TextField()
    reaction= models.CharField(max_length = 50,choices=REACTION_CHOICES, default=NONE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name.username
    
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]
