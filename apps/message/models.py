from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    """
    Conversation between two users
    """

    participants = models.ManyToManyField(User, related_name="conversations")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Conversation {self.id} - {self.participants.count()} participants"


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
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} de {self.sender.username}"
