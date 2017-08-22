from rest_framework import permissions


class IsExpertPermission(permissions.BasePermission):
    message = 'Only Experts are allowed.'

    def has_permission(self, request, views):
        return hasattr(request.user, 'expert')


class IsUserPermission(permissions.BasePermission):
    message = 'Only Users are allowed.'

    def has_permission(self, request, views):
        return hasattr(request.user, 'user')


class IsSuperUser(permissions.BasePermission):
    message = 'Only superusers are allowed.'

    def has_permission(self, request, views):
        return request.user.is_superuser


class IsSuperUserOrReadOnly(IsSuperUser):
    message = 'Only superusers are allowed.'

    def has_permission(self, request, views):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super(IsSuperUserOrReadOnly, self).has_permission(request, views)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow expert of an object to edit it.
    Assumes the model instance has an `expert` attribute.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(request.user, 'expert'):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.expert == request.user.expert
