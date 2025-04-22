from django.db import models


class City(models.Model):
    """
    Represents the city where the user lives.
    """

    name = models.CharField(unique=True, max_length=200)
    zip_code = models.CharField(unique=True, max_length=10)
    country = models.CharField(default="france")

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
