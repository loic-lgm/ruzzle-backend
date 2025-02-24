from rest_framework import serializers

from exchange.models import Exchange
from puzzle.serializers import PuzzleSerializer
from user.serializers import UserSerializer


class ExchangeSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    puzzle_asked = PuzzleSerializer(read_only=True)

    class Meta:
        model = Exchange
        fields = [
            "id",
            "status",
            "owner",
            "created",
            "updated",
            "puzzle_asked",
            "puzzle_proposed",
        ]

    def validate(self, data):
        puzzle_asked = data.get("puzzle_asked")
        puzzle_proposed = data.get("puzzle_proposed")
        owner = data.get("owner")
        user = self.context["request"].user

        if puzzle_asked and puzzle_asked.owner == user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas échanger un puzzle dont vous êtes déjà propriétaire."
            )

        if puzzle_proposed and puzzle_proposed.owner != owner:
            raise serializers.ValidationError(
                f"Vous ne pouvez proposer à l'échange qu'un puzzle appartenant à {owner.username}"
            )

        return data
