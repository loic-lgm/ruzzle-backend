from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from apps.utils.authentication import CookieJWTAuthentication
from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_read=False)[:20]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
