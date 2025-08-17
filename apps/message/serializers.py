from rest_framework import serializers

from apps.exchange.serializers import ExchangeSerializer
from apps.user.serializers import UserSerializer
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "user", "content", "created", "is_read"]
        read_only_fields = ["id", "user", "created"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    exchange = ExchangeSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "last_message",
            "created",
            "updated",
            "exchange",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created").first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_messages(self, obj):
        last_messages = obj.messages.order_by("-created")[:30]
        return MessageSerializer(last_messages, many=True).data
