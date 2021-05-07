from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS:
            return True
        elif request.user == obj.creator:
            return True
        else:
            return False
