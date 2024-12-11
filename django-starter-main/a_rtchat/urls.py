from allauth.urls import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns =[
    path('',chat_view,name='home'),
    path('start-chat/<username>',get_chatroom,name='start-chat'),
    path('chat/<chatroom_name>',chat_view,name='private-chat'),
    path('chat/new_groupchat/',create_groupchat,name='new-groupchat'),
    path('chatroom-edit/<chatroom_name>',chatroom_edit_view, name="edit-chatroom"),
    path('chatroom-delete/<chatroom_name>',chatroomdelete,name='chatroom-delete'),
    path('leave-chatroom/<chatroom_name>',leavechatroom,name='leave-chatroom'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)