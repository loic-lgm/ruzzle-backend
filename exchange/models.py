from django.db import models

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
    puzzle_asked = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name="exchanges_asked")
    puzzle_proposed = models.ForeignKey(Puzzle, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.status
