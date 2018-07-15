from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class MainConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'main_channel'
        self.room_group_name = 'main_channel'
        print('connect')
        # Join room group

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.channel_layer.group_add)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        message = text_data['message']
        print('recive')
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def new_post(self, message):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
