from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by(
            "-updated_at"
        )

    def perform_create(self, serializer):
        participants_ids = self.request.data.get("participants", [])
        conversation = serializer.save()
        if participants_ids:
            conversation.participants.add(*participants_ids)
        conversation.participants.add(
            self.request.user
        )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=self.request.user,
            ).order_by("created_at")
        return Message.objects.none()

    def perform_create(self, serializer):
        # L'utilisateur connecté est l'expéditeur
        serializer.save(user=self.request.user)
