from rest_framework import permissions

from experchat.permissions import IsOwnerOrReadOnly


class IsFeedOwnerOrReadOnly(IsOwnerOrReadOnly):
    """
    Object-level permission to only allow owner of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
