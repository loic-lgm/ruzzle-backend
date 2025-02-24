from rest_framework import serializers

from puzzle.serializers import PuzzleSerializer
from rate.models import Rate
from user.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    puzzle = PuzzleSerializer()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Rate
        fields = ["id", "owner", "puzzle"]

    def validate(self, data):
        owner = data.get("owner")
        user = self.context["request"].user

        if owner and owner == user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas ajouter votre puzzle en favoris."
            )

        return data
