import json
from email import message_from_string

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import *


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup,group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author = self.user,
            group = self.chatroom
        )
        message.save()
        event = {
            'type' : "message_handler",
            'message_id' : message.id
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    def message_handler(self, event):
        message_id=event['message_id']
        message = get_object_or_404(GroupMessage,id=message_id)
        context = {
            'msg': message,
            'user': self.user
        }
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )