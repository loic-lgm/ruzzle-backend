from rest_framework import serializers

from puzzle.models import Puzzle


class PuzzleSerializer(serializers.ModelSerializer):
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
        ]
