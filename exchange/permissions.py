from rest_framework import permissions


class IsExchangeRequested(permissions.BasePermission):
    """
    Custom permission for the user to whom an exchange has been proposed
    """

    def has_object_permission(self, request, view, obj):
        return obj.puzzle_asked.owner == request.user
