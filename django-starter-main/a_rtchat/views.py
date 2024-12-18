from os import remove

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

@login_required
def chat_view(request, chatroom_name='public-chat'):
    form = ChatmessageCreateForm()
    chatgroup = get_object_or_404(ChatGroup,group_name=chatroom_name)
    other_user = None
    if chatgroup.is_private:
        if request.user not in chatgroup.members.all():
            raise Http404()
        for mem in chatgroup.members.all():
            if mem != request.user:
                other_user=mem
    messages = chatgroup.chat_messages.all()
    if chatgroup.groupchat_name:
        if request.user not in chatgroup.members.all():
            chatgroup.members.add(request.user)
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chatgroup
            message.save()
            context = {
                'msg' : message,
                'user' : request.user
            }
            return render(request,'a_rtchat/partials/chat_message_p.html',context)
    context={
        'messages':messages,
        'form':form,
        'other_user':other_user,
        'chatroom_name':chatroom_name,
        'chatgroup' : chatgroup
    }
    return render(request,'a_rtchat/chat.html',context)

def get_chatroom(request,username):
    other_user = get_object_or_404(User,username=username)
    private_room=ChatGroup.objects.filter(is_private=True)
    for room in private_room:
        if other_user in room.members.all():
            if request.user in room.members.all():
                return redirect('private-chat',room.group_name)
    room = ChatGroup.objects.create(is_private=True)
    room.members.add(request.user)
    room.members.add(other_user)
    return redirect('private-chat', room.group_name)
def create_groupchat(request):
    form = NewGroupForm()
    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            chatroom_name = new_groupchat.group_name
            return redirect('private-chat',chatroom_name)
    context = {
        'form': form,
    }
    return render(request,'a_rtchat/create_groupchat.html',context)
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form = ChatRoomEditForm(instance=chat_group)
    if request.method == "POST":
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            for mem in remove_members:
                member = get_object_or_404(User,id=mem)
                chat_group.members.remove(member)
            return redirect('private-chat',chatroom_name)
    context = {
        'form': form,
        'chat_group' : chat_group,
    }
    return render(request,'a_rtchat/chatroom_edit.html',context)
def chatroomdelete(request, chatroom_name):
     chatroom = get_object_or_404(ChatGroup,group_name=chatroom_name)
     if request.user != chatroom.admin:
         raise Http404()
     if request.method == "POST":
          chatroom.delete()
          return redirect('home')
     return render(request,'a_rtchat/chatroom_delete.html',{'chatroom' : chatroom})
def leavechatroom(request,chatroom_name):
    chatroom = get_object_or_404(ChatGroup,group_name=chatroom_name)
    if request.user not in chatroom.members.all():
        raise Http404()
    if request.method == "POST":
        chatroom.members.remove(request.user)
        return redirect('home')