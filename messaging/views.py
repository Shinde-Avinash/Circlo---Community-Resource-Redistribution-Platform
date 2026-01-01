from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Conversation, Message
from resources.models import Resource
from .forms import MessageForm

@login_required
def inbox(request):
    conversations = request.user.conversations.all().order_by('-updated_at')
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def start_conversation(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    
    if resource.donor == request.user:
        messages.warning(request, "You cannot message yourself!")
        return redirect('resource_detail', pk=resource.id)
    
    # Check if conversation already exists
    # We filter conversations for this resource that contain the current user
    existing_chat = Conversation.objects.filter(resource=resource, participants=request.user).first()
    
    if existing_chat:
        return redirect('chat_detail', pk=existing_chat.id)
    
    # Create new conversation
    chat = Conversation.objects.create(resource=resource)
    chat.participants.add(request.user, resource.donor)
    return redirect('chat_detail', pk=chat.id)

@login_required
def chat_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not a participant in this chat.")
    
    form = MessageForm()
    chat_messages = conversation.messages.all()
    
    # Mark messages as read (simple logic: all messages from other user)
    # in a real app, we'd filter by is_read=False
    
    if request.headers.get('HX-Request'):
        return render(request, 'messaging/message_list_partial.html', {'chat_messages': chat_messages, 'user': request.user})
    
    return render(request, 'messaging/chat_room.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'form': form
    })

@login_required
def send_message(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            
            # Update conversation timestamp
            conversation.save()
            
            # Create Notification
            from notifications.models import Notification
            recipient = conversation.participants.exclude(id=request.user.id).first()
            if recipient:
                Notification.objects.create(
                    recipient=recipient,
                    actor=request.user,
                    message=f"New message from {request.user.username}",
                    link=f"/messages/chat/{conversation.id}/",
                    notification_type='message'
                )

            # Return the updated message list partial
            chat_messages = conversation.messages.all()
            return render(request, 'messaging/message_list_partial.html', {'chat_messages': chat_messages, 'user': request.user})
            
    return HttpResponseForbidden()
