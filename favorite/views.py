from django.forms import ValidationError
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer
from permissions import IsOwner
from puzzle.models import Puzzle


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "destroy"]:
            return [IsOwner()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        puzzle_id = request.data.get("puzzle_id")

        if not puzzle_id:
            return Response(
                {"error": "Vous devez choisir un puzzle."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            puzzle = Puzzle.objects.get(pk=puzzle_id)
        except Puzzle.DoesNotExist:
            return Response(
                {"error": "Le puzzle choisi n'existe pas."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if puzzle.owner == self.request.user:
            return Response(
                {"error": "Vous ne pouvez pas mettre en favori votre propre puzzle."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        already_exists = Favorite.objects.filter(
            owner=self.request.user, puzzle=puzzle
        ).exists()

        if already_exists:
            return Response(
                {"error": "Ce puzzle est déjà dans vos favoris."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user, puzzle=puzzle)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
