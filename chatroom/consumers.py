# chat/consumers.py
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from users.models import UserProfile

from .models import Message,Channel
from .serializers import  MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def getUser(self,userID):
        return UserProfile.objects.get(id=userID)

    @sync_to_async
    def getChannel(self, channelName):
        return Channel.objects.get(name=channelName)


    def getMessage(self, userID):
        return UserProfile.objects.get(id=userID)

    @sync_to_async
    def saveMessage(self,message):
        message.save()
        return message

    @sync_to_async
    def serializeMessage(self, message):
        serializer = MessageSerializer(message)
        print(serializer.data);
        return serializer.data

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Join room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]

        #Handle Database Logic

        channel = await self.getChannel(self.room_name)


        message = Message(content=message, sent_by_id=user_id, channel=channel)
        message = await self.saveMessage(message)
        message_data = await self.serializeMessage(message)


        #Send the message to a channel under 'room_name'
        await self.channel_layer.group_send(
            self.room_name, {"type": "group_message", "message": message_data}
        )

    # Receive message from room group
    async def group_message(self, event):
        message = event["message"]
        print(event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))