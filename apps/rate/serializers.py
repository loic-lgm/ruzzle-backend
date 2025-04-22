from rest_framework import serializers

from apps.exchange.serializers import ExchangeSerializer
from apps.rate.models import Rate
from apps.user.serializers import UserSerializer


class RateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    reviewed = UserSerializer()
    rating = serializers.IntegerField(min_value=0, max_value=5)
    exchange = ExchangeSerializer(read_only=True)

    class Meta:
        model = Rate
        fields = ["id", "rating", "comment", "owner", "reviewed", "exchange", "created"]

    def validate(self, data):
        exchange = data.get("exchange")
        user = self.context["request"].user

        if not exchange and exchange.status == "accepted":
            raise serializers.ValidationError(
                "Vous ne pouvez pas émettre un avis si l'échange n'est pas accepté."
            )
        if exchange and (exchange.owner == user or exchange.puzzle_asked.owner):
            raise serializers.ValidationError(
                "Vous ne pouvez pas émettre un avis sur cet échange."
            )

        return data
