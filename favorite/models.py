from django.db import models

from puzzle.models import Puzzle
from user.models import User


class Favorite(models.Model):
    """
    Represents an user's favorite.
    """
    
    created = models.DateTimeField(auto_now_add=True)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name="puzzle")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Favorite: {self.owner.username} - Puzzle {self.puzzle.name}"
