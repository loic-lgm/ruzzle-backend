from rest_framework import permissions, viewsets

from exchange.models import Exchange
from exchange.permissions import IsExchangeRequested
from exchange.serializers import ExchangeSerializer
from permissions import IsOwner


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     print("-------SERIALIZER-------")
    #     print(serializer.data)
    #     puzzle_asked = serializer.initial_data.get("puzzle_asked")

    #     if puzzle_asked:
    #         print("-------PUZZLE ASKED--------")
    #         print(puzzle_asked)
    #         owner = puzzle_asked.owner
    #         serializer.save(requester=self.request.user, owner=owner)
    #     else:
    #         raise serializer.ValidationError("Vous devez demander un puzzle.")

    #TODO OVERWRITE CREATE
    # Recuperer le puzzle_asked avec la request ou validated_data.
    # Faire un Puzzle.objects.filter(....) pour récuperer le puzzle
    # Associer le puzzle_asked.owner=owner
    # Associer request.user=requester
    
