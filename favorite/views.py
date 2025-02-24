from rest_framework import permissions, viewsets

from favorite.models import Favorite
from rate.serializers import RateSerializer
from permissions import IsOwnerOrReadOnly

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser, IsOwnerOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
