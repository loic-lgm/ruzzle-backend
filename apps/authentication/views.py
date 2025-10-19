from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers import RegisterSerializer
from apps.user.serializers import UserSerializer
from apps.utils.authentication import CookieJWTAuthentication
from apps.user.utils import generate_activation_link, generate_forgot_password_link
from apps.utils.send_email import send_activation_email, send_reset_password_email

User = get_user_model()


class AuthenticationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
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
                {"error": "Identifiants invalides"},
                status=status.HTTP_401_UNAUTHORIZED,
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
            secure=True,
            samesite="None",
            max_age=3600,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            max_age=3600 * 24 * 7,
            path="/",
        )
        return response

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(
                {"message": "Déconnexion réussie"}, status=status.HTTP_200_OK
            )
            response.delete_cookie("access_token", path="/", samesite="None")
            response.delete_cookie("refresh_token", path="/", samesite="None")
            return response
        except Exception:
            return Response(
                {"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def refresh(self, request):
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
                secure=True,
                samesite="None",
                max_age=3600,
                path="/",
            )
            return response
        except Exception:
            return Response(
                {"error": "Le refresh token est invalide ou a expiré."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            activation_link = generate_activation_link(user, request)
            send_activation_email(user, activation_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_path=r"activate/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)",
    )
    def activate(self, request, uidb64=None, token=None):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST
            )
        if default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({"message": "Compte déjà activé."})
            user.is_active = True
            user.save()
            return Response({"message": "Compte activé avec succès !"})
        else:
            return Response(
                {"error": "Lien invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=["get"],
        authentication_classes=[CookieJWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=200)

    @action(
        detail=False,
        methods=["post"],
        url_path=r"reset-password/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)",
    )
    def reset_password(self, request, uidb64=None, token=None):
        new_password = request.data.get("password")
        if not new_password:
            return Response(
                {"error": "Le nouveau mot de passe est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST
            )
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Mot de passe réinitialisé avec succès !"})
        else:
            return Response(
                {"error": "Lien invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        url_path="forgot-password",
    )
    def forgot_password(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST
            )
        response_message = {
            "message": "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé."
        }
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(response_message, status=status.HTTP_200_OK)
        reset_link = generate_forgot_password_link(user, request)
        send_reset_password_email(user, reset_link)
        return Response(response_message, status=status.HTTP_200_OK)
