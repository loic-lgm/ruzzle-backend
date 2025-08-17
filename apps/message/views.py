from re import S
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from django.db.models import Prefetch

from apps.notification.models import Notification
from apps.utils.authentication import CookieJWTAuthentication
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


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
            raise PermissionDenied(
                "Vous ne pouvez pas envoyer de message dans cette conversation."
            )
        serializer.save(user=self.request.user)
        conversation.save(update_fields=["updated"])
        other_participant = conversation.participants.exclude(
            id=self.request.user.id
        ).first()
        if other_participant:
            Notification.objects.create(
                user=other_participant,
                sender=self.request.user,
                notif_type="new_message",
            )

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        conversations = Conversation.objects.filter(
            participants=request.user
        ).prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.order_by("-created"),
                to_attr="prefetched_messages",
            )
        )
        count = 0
        for conv in conversations:
            last_msg = conv.prefetched_messages[0] if conv.prefetched_messages else None
            if last_msg and last_msg.user != request.user and not last_msg.is_read:
                count += 1

        return Response({count})
