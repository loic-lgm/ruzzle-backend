from django.db import models


class Brand(models.Model):
    """
    Represents a puzzle brand.
    """

    name = models.CharField(unique=True, max_length=255)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
