from rest_framework import serializers

from exchange.models import Exchange
from puzzle.serializers import PuzzleSerializer
from user.serializers import UserSerializer


class ExchangeSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    requester = UserSerializer(read_only=True)
    puzzle = PuzzleSerializer(read_only=True)
    
    class Meta:
        model = Exchange
        fields = [
            "id",
            "status",
            "puzzle",
            "requester",
            "owner",
            "created",
            "updated",
        ]
