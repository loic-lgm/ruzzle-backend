from rest_framework import permissions, viewsets

from permissions import IsOwnerOrIsAdminOrReadOnly
from puzzle.models import Puzzle
from puzzle.serializers import PuzzleSerializer


class PuzzleViewSet(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrIsAdminOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
