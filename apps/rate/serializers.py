from rest_framework import serializers

from apps.exchange.models import Exchange
from apps.rate.models import Rate
from apps.user.models import User
from apps.user.serializers import UserSerializer


class RateSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    reviewed = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    rating = serializers.IntegerField(min_value=0, max_value=5)
    exchange = serializers.PrimaryKeyRelatedField(
        queryset=Exchange.objects.all(), write_only=True
    )

    class Meta:
        model = Rate
        fields = ["id", "rating", "comment", "owner", "reviewed", "exchange", "created"]

    def validate(self, data):
        exchange = data.get("exchange")
        user = self.context["request"].user
        if not exchange:
            raise serializers.ValidationError("Exchange invalide.")
        if exchange.status != "accepted":
            raise serializers.ValidationError(
                "Vous ne pouvez émettre un avis que sur un échange accepté."
            )
        if user != exchange.requester and user != exchange.owner:
            raise serializers.ValidationError(
                "Vous n'êtes pas participant à cet échange."
            )
        if data.get("reviewed") == user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas vous noter vous-même."
            )
        if Rate.objects.filter(owner=user, exchange=exchange).exists():
            raise serializers.ValidationError("Vous avez déjà noté cet échange.")
        return data
