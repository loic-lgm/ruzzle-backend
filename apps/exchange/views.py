from rest_framework import mixins, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.exchange.models import Exchange
from apps.exchange.permissions import IsExchangeRequestedOrRequester
from apps.exchange.serializers import ExchangeSerializer
from apps.message.models import Conversation, Message
from apps.notification.models import Notification
from apps.puzzle.models import Puzzle


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
        message = request.data.get("message")

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
            message=message,
        )

        puzzle_asked.status = "pending"
        puzzle_asked.save()
        puzzle_proposed.status = "pending"
        puzzle_proposed.save()

        Notification.objects.create(
            user=puzzle_asked.owner, sender=request.user, notif_type="exchange_request"
        )

        exchange = serializer.instance
        conversation = Conversation.objects.create(exchange=exchange)
        conversation.participants.add(request.user, puzzle_asked.owner)
        if message:
            Message.objects.create(
                conversation=conversation, user=request.user, content=message
            )
            Notification.objects.create(
                user=puzzle_asked.owner,
                sender=request.user,
                notif_type="new_message",
                conversation=conversation,
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        from django.db.models import Q

        instance = self.get_object()
        old_status = instance.status
        conversation = instance.conversation
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        new_status = serializer.validated_data.get("status")
        if new_status == "accepted" and old_status != "accepted":
            instance.status = "accepted"
            instance.save()
            puzzle_asked = instance.puzzle_asked
            puzzle_proposed = instance.puzzle_proposed
            if puzzle_asked:
                puzzle_asked.status = "swapped"
                puzzle_asked.save()
            if puzzle_proposed:
                puzzle_proposed.status = "swapped"
                puzzle_proposed.save()
            other_exchanges = (
                Exchange.objects.filter(
                    Q(puzzle_asked=puzzle_asked)
                    | Q(puzzle_proposed=puzzle_asked)
                    | Q(puzzle_asked=puzzle_proposed)
                    | Q(puzzle_proposed=puzzle_proposed)
                )
                .exclude(id=instance.id)
                .select_related("conversation")
            )
            Notification.objects.create(
                user=puzzle_proposed.owner,
                sender=request.user,
                notif_type="exchange_accepted",
                conversation=conversation,
            )
            for exchange in other_exchanges:
                exchange.status = "denied"
                exchange.save()
                # if hasattr(exchange, "conversation"):
                # Message.objects.create(
                #     conversation=exchange.conversation,
                #     user=request.user,
                #     content="Bonjour, j'ai accepté une autre offre pour ce puzzle.",
                # )
                other_user = (
                    exchange.puzzle_proposed.owner
                    if request.user != exchange.puzzle_proposed.owner
                    else exchange.puzzle_asked.owner
                )
                Notification.objects.create(
                    user=other_user,
                    sender=request.user,
                    notif_type="exchange_denied",
                    conversation=conversation,
                )

        if new_status == "denied" and old_status != "denied":
            puzzle_asked = instance.puzzle_asked
            puzzle_proposed = instance.puzzle_proposed
            other_user = (
                instance.puzzle_proposed.owner
                if request.user != instance.puzzle_proposed.owner
                else instance.puzzle_asked.owner
            )
            for puzzle in [puzzle_asked, puzzle_proposed]:
                if puzzle:
                    is_in_other_exchange = (
                        Exchange.objects.filter(
                            Q(puzzle_asked=puzzle) | Q(puzzle_proposed=puzzle),
                        )
                        .exclude(id=instance.id)
                        .exclude(status="denied")
                        .exists()
                    )

                    if not is_in_other_exchange:
                        puzzle.status = "available"
                        puzzle.save()
            Notification.objects.create(
                user=other_user,
                sender=request.user,
                notif_type="exchange_denied",
                conversation=conversation,
            )

        return Response(self.get_serializer(instance).data)
