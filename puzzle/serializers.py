from rest_framework import serializers

from puzzle.models import Puzzle
from user.serializers import UserSerializer


class PuzzleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Puzzle
        fields = [
            "id",
            "name",
            "brand",
            "piece_count",
            "description",
            "condition",
            "image_url",
            "status",
            "is_published",
            "owner",
        ]
