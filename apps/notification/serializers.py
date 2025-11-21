from rest_framework import serializers
from apps.notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    conversation_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "notif_type",
            "sender_username",
            "is_read",
            "created_at",
            "conversation_id",
        ]

    def get_conversation_id(self, obj):
        return obj.conversation.id if obj.conversation else None
