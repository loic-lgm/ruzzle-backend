from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from apps.exchange.models import Exchange
from apps.puzzle.serializers import PuzzleSerializer
from apps.user.serializers import UserSerializer
from apps.rate.models import Rate


class ExchangeSerializer(serializers.ModelSerializer):
    puzzle_asked = PuzzleSerializer(read_only=True)
    puzzle_proposed = PuzzleSerializer(read_only=True)
    puzzle_asked_id = serializers.IntegerField(write_only=True, required=True)
    puzzle_proposed_id = serializers.IntegerField(write_only=True, required=False)
    message = serializers.CharField(required=False)
    requester = UserSerializer(read_only=True)
    conversation_id = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Exchange
        fields = [
            "id",
            "created",
            "status",
            "puzzle_asked",
            "puzzle_proposed",
            "puzzle_asked_id",
            "puzzle_proposed_id",
            "message",
            "requester",
            "conversation_id",
            "has_voted",
        ]

    def get_has_voted(self, obj):
        user = self.context["request"].user
        return Rate.objects.filter(exchange=obj, owner=user).exists()

    def get_conversation_id(self, obj):
        try:
            return obj.conversation.id
        except ObjectDoesNotExist:
            return None

    def validate(self, data):
        if self.instance:
            return data

        puzzle_asked_id = data.get("puzzle_asked_id")
        puzzle_proposed_id = data.get("puzzle_proposed_id")

        if puzzle_asked_id and puzzle_proposed_id:
            already_exists = (
                Exchange.objects.filter(
                    puzzle_asked_id=puzzle_asked_id,
                    puzzle_proposed_id=puzzle_proposed_id,
                )
                .exclude(status="denied")
                .exists()
            )

            if already_exists:
                raise serializers.ValidationError(
                    {"error": "Un échange avec ces puzzles existe déjà."}
                )
        return data
