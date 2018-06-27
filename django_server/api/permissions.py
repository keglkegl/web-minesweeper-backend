from rest_framework import permissions


class IsOwnerEmptyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow players of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return (((obj.player1 == request.user) or (obj.player1 == None)) or ((obj.player2 == request.user) or (obj.player2 == None)))

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow players of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return (obj == request.user)

        # Write permissions are only allowed to the owner of the snippet.
        return (obj == request.user)

class ReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow players of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return (obj == request.user)

        # Write permissions are only allowed to the owner of the snippet.
        return False
