from rest_framework import serializers

from apps.user.serializers import UserSerializer
from .models import Conversation, Message
from django.contrib.auth import get_user_model


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "user", "content", "created_at", "is_read"]
        read_only_fields = ["id", "user", "created_at", "is_read"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "last_message",
            "created_at",
            "updated_at",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_messages(self, obj):
        last_messages = obj.messages.order_by("-created_at")[:30]
        return MessageSerializer(last_messages, many=True).data
