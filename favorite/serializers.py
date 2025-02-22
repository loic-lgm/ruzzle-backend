from rest_framework import serializers

from puzzle.serializers import PuzzleSerializer
from rate.models import Rate
from user.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    puzzle = PuzzleSerializer()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Rate
        fields = ["id", "owner", "puzlle"]
