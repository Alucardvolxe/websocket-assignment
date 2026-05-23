import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

from .models import Message, Room


#To-do make users unique perchat-room
class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.filter(room=self.room).order_by('-timestamp')
        content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = (data.get('from') or '').strip()

        if not author:
            self.send(text_data=json.dumps({'error': 'No username provided'}))
            return

        author_user, created = User.objects.get_or_create(username=author)

        message = Message.objects.create(
            author=author_user,
            message=data['message'],
            reaction=data.get('reaction', ''),
            room=self.room, 
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        return [self.message_to_json(m) for m in messages]

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'message': message.message,
            'reaction': message.reaction,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
   
        self.room, created = Room.objects.get_or_create(room_name=self.room_name)
        self.room_group_name = f"chat_{self.room_name}"  

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()




    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['commands']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat.message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))