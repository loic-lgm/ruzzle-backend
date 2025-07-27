from rest_framework import serializers

from apps.exchange.models import Exchange
from apps.puzzle.serializers import PuzzleSerializer


class ExchangeSerializer(serializers.ModelSerializer):
    puzzle_asked = PuzzleSerializer(read_only=True)
    puzzle_proposed = PuzzleSerializer(read_only=True)
    puzzle_asked_id = serializers.IntegerField(write_only=True, required=True)
    puzzle_proposed_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Exchange
        fields = [
            "created",
            "status",
            "puzzle_asked",
            "puzzle_proposed",
            "puzzle_asked_id",
            "puzzle_proposed_id",
            "message",
        ]

    def validate(self, data):
        if self.instance:
            return data

        puzzle_asked_id = data.get("puzzle_asked_id")
        puzzle_proposed_id = data.get("puzzle_proposed_id")

        if puzzle_asked_id and puzzle_proposed_id:
            already_exists = Exchange.objects.filter(
                puzzle_asked_id=puzzle_asked_id, puzzle_proposed_id=puzzle_proposed_id
            ).exists()

            if already_exists:
                raise serializers.ValidationError(
                    "Un échange avec ces puzzles existe déjà."
                )
