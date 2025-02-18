from django.contrib.auth import get_user_model
from user.serializers import UserSerializer
from rest_framework import permissions, viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list"]:
            return [permissions.IsAdminUser]
        elif self.action in ["create", "update", "partial_update"]:
            return []
        return super().get_permissions()
