from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

@login_required
def chat_view(request):
    form = ChatmessageCreateForm()
    chatgroup=get_object_or_404(ChatGroup,group_name='public-chat')
    messages = chatgroup.chat_messages.all()
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
    return render(request,'a_rtchat/chat.html',{'messages':messages,'form':form})