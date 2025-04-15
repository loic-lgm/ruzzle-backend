from django.contrib.auth import authenticate, get_user_model

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserRegistrationSerializer, UserSerializer


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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    except Exception:
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

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data,
            }
        )
    else:
        return Response(
            {"error": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
