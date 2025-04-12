from argparse import Action
from sre_constants import AT_UNI_NON_BOUNDARY
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from exchange.models import Exchange
from exchange.permissions import IsExchangeRequestedOrRequester
from exchange.serializers import ExchangeSerializer
from puzzle.models import Puzzle


class ExchangeViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            return [IsExchangeRequestedOrRequester()]
        return super().get_permissions()
    

    def create(self, request, *args, **kwargs):
        puzzle_asked_id = request.data.get("puzzle_asked_id")
        puzzle_proposed_id = request.data.get("puzzle_proposed_id")

        if not puzzle_asked_id:
            raise ValidationError({"error": "Vous devez demander un puzzle."})

        try:
            puzzle_asked = Puzzle.objects.get(pk=puzzle_asked_id)
        except Puzzle.DoesNotExist:
            return Response(
                {"error": "Le puzzle demandé n'existe pas."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if puzzle_asked.owner == request.user:
            return Response(
                {
                    "error": "Vous ne pouvez pas échanger un puzzle dont vous êtes déjà propriétaire."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if puzzle_proposed_id:
            try:
                puzzle_proposed = Puzzle.objects.get(pk=puzzle_proposed_id)
            except Puzzle.DoesNotExist:
                return Response(
                    {"error": "Le puzzle demandé n'existe pas."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if puzzle_proposed.owner != request.user:
            return Response(
                {
                    "error": "Vous ne pouvez proposer à l'échange qu'un puzzle vous apprtenant."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            requester=request.user,
            owner=puzzle_asked.owner,
            puzzle_asked=puzzle_asked,
            puzzle_proposed=puzzle_proposed,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

