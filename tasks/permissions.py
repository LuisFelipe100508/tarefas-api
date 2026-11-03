from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Permite acesso ao objeto apenas ao seu dono."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user