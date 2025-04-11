from rest_framework import permissions, viewsets

from rate.models import Rate
from rate.serializers import RateSerializer
from permissions import IsOwnerOrReadOnly

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUse()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
