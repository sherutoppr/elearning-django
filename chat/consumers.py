import json
from channels.generic.websocket import WebsocketConsumer
# wrap calls to asynchronous
from asgiref.sync import async_to_sync

# to add context to the message
from django.utils import timezone

# to make it asynchronous
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer( AsyncWebsocketConsumer):
    async def connect(self):  # called when a new connection s received
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']    # retrieve the course id
        self.room_group_name = 'chat_%s' % self.id                  # create the group name
        # join room group by giving the group name and channel name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()          # await used  to call asynchronous function that perform i/o operations

    async def disconnect(self, close_code):   # when socket is closed
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):   # called whenever data is received
        text_data_json = json.loads(text_data)     # load json data to python library
        message = text_data_json['message']
        now = timezone.now()

        # send message to WebSocket after transforming through json.dump()
        # self.send(text_data=json.dumps({'message': message}))
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

