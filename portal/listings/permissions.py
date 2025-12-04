from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only to anyone, but write only to owner.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.owner == request.user