from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from user.models import User


class Puzzle(models.Model):
    """
    Represents a puzzle.
    """

    BRAND_CHOICES = [
        ("ravensburger", "Ravensburger"),
        ("clementoni", "Clementoni"),
        ("jan van Haasteren", "Jan van Haasteren"),
        ("gibsons", "Gibsons"),
        ("educa", "Educa"),
        ("schmidt Spiele", "Schmidt Spiele"),
        ("buffalo Games", "Buffalo Games"),
        ("wasgij", "Wasgij"),
        ("puzzle Master", "Puzzle Master"),
        ("eurographics", "Eurographics"),
    ]

    CONDITION_CHOICES = [
        ("available", "available"),
        ("used", "used"),
        ("damaged", "damaged"),
    ]

    STATUS_CHOICES = [
        ("available", "available"),
        ("pending", "pending"),
        ("swap", "swap"),
    ]

    name = models.CharField(max_length=255)
    brand = models.CharField(choices=BRAND_CHOICES)
    piece_count = models.IntegerField()
    description = models.TextField(max_length=3000)
    condition = models.CharField(choices=CONDITION_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="available")
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="puzzles")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
