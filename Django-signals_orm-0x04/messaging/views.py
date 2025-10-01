from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .models import Message

def conversation_view(request, message_id):
    root_message = (
        Message.objects.select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
        .get(id=message_id)
    )
    thread = get_threaded_messages(root_message)
    return render(request, "messaging/conversation.html", {"thread": thread})

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("home")
