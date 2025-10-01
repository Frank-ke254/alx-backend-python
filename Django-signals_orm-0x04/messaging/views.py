from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .models import Message

@login_required
def conversation_view(request, message_id):
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver"),
        id=message_id,
        sender=request.user
    )
    thread = get_threaded_messages(root_message)
    return render(request, "messaging/conversation.html", {"thread": thread})

def get_threaded_messages(message):
    replies = Message.objects.filter(parent_message=message).select_related("sender", "receiver")
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [get_threaded_messages(reply) for reply in replies],
    }

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("home")

@login_required
def inbox_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/inbox.html", {"messages": unread_messages})
