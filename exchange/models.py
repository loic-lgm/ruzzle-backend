from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from puzzle.models import Puzzle
from user.models import User


class Exchange(models.Model):
    """
    Represents an exchange between two users.
    """

    STATUS_CHOICES = [
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("denied", "denied"),
    ]

    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanges")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exchanges_requested")
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name="puzzles")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.status
