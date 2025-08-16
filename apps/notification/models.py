from django.db import models

from apps.user.models import User


class Notification(models.Model):
    NOTIF_TYPES = [
        ("exchange_request", "Demande d'échange"),
        ("new_message", "Nouveau message"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    notif_type = models.CharField(max_length=50, choices=NOTIF_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notif_type} de {self.sender.username} à {self.user.username}"
