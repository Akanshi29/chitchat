import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from account.models import UserProfile, Contacts
from chat.models import ChatDetail, Group
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        group = await self.get_group()
        self.group_name = str(group.uuid)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # fetch previous chats to show on page
        chats = await self.get_chats()
        async for chat in chats:
            # for sending previous chats to frontend
            time = (chat.updated_at).strftime('%H:%M')
            await self.send(text_data=json.dumps({
                'type': 'previousMessages',
                'message': chat.message,
                'username': await self.fetch_sender(chat_id=chat.id),
                'time': time

            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        contact_id = text_data_json["send_to"]
        time = text_data_json["time"]
        sender = await self.get_user(username=username)
        await self.save_message(message=message, sender=sender)
        await self.channel_layer.group_send(
            self.group_name, {
                "type": "chatbox_message",
                "message": message,
                "username": username,
                "time": time
            })
    
    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]
        #send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "time": time
                }
            )
        )
    
    @database_sync_to_async
    def get_group(self):
        return Group.objects.get(id=self.group_id)

    @database_sync_to_async
    def get_user(self,username):
        return UserProfile.objects.get(user__username=username)
    
    @database_sync_to_async
    def fetch_sender(self, chat_id):
        return ChatDetail.objects.get(id=chat_id).sender.user.first_name
    
    @database_sync_to_async
    def get_chats(self):
        return ChatDetail.objects.filter(group__id=self.group_id).order_by('updated_at')

    @database_sync_to_async
    def save_message(self, message, sender):
        group = Group.objects.get(id=self.group_id)
        ChatDetail.objects.create(sender=sender, message=message, group=group)
        group_members = group.members.exclude(id=sender.id).first()
        contacts = Contacts.objects.filter(user=group_members, user_member=sender).first()
        if not contacts:
            Contacts.objects.create(user=group_members, user_member=sender, chat_initated=True)
     