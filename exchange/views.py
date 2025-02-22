from rest_framework import permissions, viewsets

from exchange.models import Exchange
from exchange.serializers import ExchangeSerializer
from permissions import IsOwnerOrReadOnly

class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [permissions.IsAdminUser, IsOwnerOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
