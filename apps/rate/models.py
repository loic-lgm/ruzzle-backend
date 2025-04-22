from django.db import models

from apps.exchange.models import Exchange
from apps.user.models import User


class Rate(models.Model):
    """
    Represents an user rating.
    """

    rating = models.IntegerField()
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates_given")
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates_received")
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.rating)
