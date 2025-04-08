from rest_framework import permissions, viewsets

from exchange.models import Exchange
from exchange.permissions import IsExchangeRequested
from exchange.serializers import ExchangeSerializer
from permissions import IsOwner


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [
        permissions.IsAdminUser,
        IsOwner,
        IsExchangeRequested,
    ]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
