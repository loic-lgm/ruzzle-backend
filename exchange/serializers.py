from rest_framework import serializers

from exchange.models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
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
