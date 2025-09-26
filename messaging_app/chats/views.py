from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .permissions import IsMessageOwner, IsConversationParticipant
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from .pagination import MessagePagination                                                                                                                                                                                                                                                                                 


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsConversationParticipant]
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "At least one participant is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = User.objects.filter(id__in=participant_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsMessageOwner]
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = MessageFilter 
    search_fields = ["participants__email"]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response({"error": "conversation and message_body required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, id=conversation_id)

        sender = request.user if request.user.is_authenticated else None
        if not sender:
            return Response({"error": "Authentication required."},
                            status=status.HTTP_401_UNAUTHORIZED)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)


    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            return Response(
                {"error": "Invalid! Not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)
