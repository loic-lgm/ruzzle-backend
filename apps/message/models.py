from django.db import models
from django.conf import settings

from apps.exchange.models import Exchange

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    """
    Conversation between two users
    """

    exchange = models.OneToOneField(
        Exchange, on_delete=models.CASCADE, related_name="conversation"
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation pour échange {self.exchange_id}"


class Message(models.Model):
    """
    Message sent by a user in a conversation
    """

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent"
    )
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} de {self.user.username}"
