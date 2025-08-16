from rest_framework import viewsets, permissions

from apps.utils.authentication import CookieJWTAuthentication
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )[:20]
