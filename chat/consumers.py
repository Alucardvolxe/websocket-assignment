import json
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from .models import Message

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages(messages)

        content = {
            'messages': self.messages_to_json(messages)
        }
    
    def new_message(self, data):
        print('new message')
        

    def messages_to_json(self,messages):
        result =[]
        for message in messages:
            result.append(self.message_to_json(message))

        return result
    

    def message_to_json(self, message):
        return {
            ''
        }
    commands = {
        'fetch_messages': fetch_messages,
        'new_messages':new_message, 
    }
     

    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['commands']](self,data)
        

    def send_chat_message(self,message):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message", 
                "message": message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))