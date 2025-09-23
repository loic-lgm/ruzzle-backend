from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode


from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.exchange.models import Exchange
from apps.exchange.serializers import ExchangeSerializer
from apps.favorite.models import Favorite
from apps.favorite.serializers import FavoriteSerializer
from apps.user.utils import generate_activation_link
from apps.utils.authentication import CookieJWTAuthentication
from apps.utils.permissions import IsOwnerParam
from apps.user.models import User
from apps.user.serializers import (
    UserPublicSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from apps.utils.send_email import send_activation_email


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
        users = User.objects.filter(username__istartswith=search)
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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response(
            {"message": "Déconnexion réussie"}, status=status.HTTP_200_OK
        )
        response.delete_cookie(
            key="access_token",
            path="/",
            samesite="None",
        )
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="None",
        )
        return response
    except Exception as e:
        print(e)
        return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    password = request.data.get("password")
    email = request.data.get("email")
    if not email or not password:
        return Response(
            {"error": "Veuillez fournir un email et un mot de passe"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(username=email, password=password)
    if user is None:
        return Response(
            {"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED
        )
    if not user.is_active:
        return Response(
            {
                "error": "Votre compte n'est pas encore activé. Veuillez vérifier vos emails."
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    response = Response(
        {"message": "Connexion réussie", "user": UserSerializer(user).data},
        status=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # True HTTPS
        samesite="None",
        max_age=3600,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=True,  # True HTTPS only
        samesite="None",
        max_age=3600 * 24 * 7,
        path="/",
    )
    return response


@api_view(["POST"])
def refresh(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "Refresh token non trouvé dans les cookies."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        response = Response(
            {"message": "Access token renouvelé."}, status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # True HTTPS only
            samesite="None",
            max_age=3600,
            path="/",
        )
        return response

    except Exception as e:
        return Response(
            {"error": "Le refresh token est invalide ou a expiré."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
def register(request):
    serializer = UserRegistrationSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        user = serializer.save()
        activation_link = generate_activation_link(user, request)
        send_activation_email(user, activation_link)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST)
    if default_token_generator.check_token(user, token):
        if user.is_active:
            return Response({"message": "Compte déjà activé."})
        user.is_active = True
        user.save()
        return Response({"message": "Compte activé avec succès !"})
    else:
        return Response(
            {"error": "Lien invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user, context={"request": request})
    return Response(serializer.data, status=200)


@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    if request.user.username == username:
        return Response(
            {"error": "Utilisez la route /mon-espace pour accéder à votre profil."},
            status=403,
        )
    try:
        user = User.objects.get(username=username)
        serializer = UserPublicSerializer(user, context={"request": request})
        return Response(serializer.data, status=200)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur introuvable"}, status=404)
