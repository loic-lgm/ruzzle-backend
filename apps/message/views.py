from rest_framework import mixins, viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.utils.authentication import CookieJWTAuthentication
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q


class ConversationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by(
            "-updated"
        )


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by("created")

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("Vous ne pouvez pas envoyer de message dans cette conversation.")
        serializer.save(user=self.request.user)
