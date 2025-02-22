from django.db import models

from exchange.models import Exchange
from user.models import User


class Rate(models.Model):
    """
    Represents an user rating.
    """
    
    rating = models.IntegerField()
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed")
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name="exchanges")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.rating
