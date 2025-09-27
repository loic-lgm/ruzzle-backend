from django.contrib.auth import get_user_model
from django.db.models import Q


from rest_framework import mixins, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.exchange.models import Exchange
from apps.exchange.serializers import ExchangeSerializer
from apps.favorite.models import Favorite
from apps.favorite.serializers import FavoriteSerializer
from apps.utils.authentication import CookieJWTAuthentication
from apps.utils.permissions import IsOwnerParam
from apps.user.models import User
from apps.user.serializers import (
    UserPublicSerializer,
    UserSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["update"]:
            user_id = self.kwargs.get("pk")
            if str(self.request.user.id) != user_id:
                raise PermissionDenied(
                    "Vous ne pouvez modifier que votre propre profil."
                )
            return [IsAuthenticated()]

        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def search(self, request):
        search = request.query_params.get("q", "")
        if not search:
            return Response([])
        users = User.objects.filter(
            username__istartswith=search, is_active=True
        ).exclude(is_staff=True, is_superuser=True)
        if request.user.is_authenticated:
            users = users.exclude(id=request.user.id)
        users = users[:10]
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[IsOwnerParam])
    def favorites(self, request, pk=None):
        user = self.get_object()
        favorites = Favorite.objects.filter(owner=user)
        serializer = FavoriteSerializer(
            favorites, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsOwnerParam],
        url_path="requested-exchanges",
    )
    def requested_exchange(self, request, pk=None):
        user = self.get_object()
        exchanges = Exchange.objects.filter(owner=user, status="pending")
        serializer = ExchangeSerializer(
            exchanges, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsOwnerParam],
        url_path="requester-exchanges",
    )
    def requester_exchange(self, request, pk=None):
        user = self.get_object()
        exchanges = Exchange.objects.filter(requester=user, status="pending")
        serializer = ExchangeSerializer(
            exchanges, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsOwnerParam],
        url_path="completed-exchanges",
    )
    def completed_exchange(self, request, pk=None):
        user = self.get_object()
        exchanges = Exchange.objects.filter(status="accepted").filter(
            Q(requester=user) | Q(owner=user)
        )

        serializer = ExchangeSerializer(
            exchanges, many=True, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([AllowAny])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(
            username=username, is_active=True, is_staff=False, is_superuser=False
        )
    except User.DoesNotExist:
        return Response({"error": "Utilisateur introuvable"}, status=404)
    if request.user.is_authenticated and request.user.username == username:
        return Response(
            {"error": "Utilisez la route /mon-espace pour accéder à votre profil."},
            status=403,
        )
    serializer = UserPublicSerializer(user, context={"request": request})
    return Response(serializer.data, status=200)
