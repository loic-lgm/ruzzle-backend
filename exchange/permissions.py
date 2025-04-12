from rest_framework import permissions


class IsExchangeRequestedOrRequester(permissions.BasePermission):
    """
    Personalized authorization for the user to whom an exchange
    has been proposed or who has proposed an exchange
    """

    def has_object_permission(self, request, view, obj):
        return obj.puzzle_asked.owner == request.user or (
            obj.puzzle_proposed.owner and obj.puzzle_proposed.owner == request.user
        )
