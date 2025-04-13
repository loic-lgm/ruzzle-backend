from rest_framework import serializers

from puzzle.serializers import PuzzleSerializer
from favorite.models import Favorite
from user.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    puzzle = PuzzleSerializer(read_only=True)
    puzzle_id = serializers.IntegerField(write_only=True, required=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "owner", "puzzle", "puzzle_id"]
