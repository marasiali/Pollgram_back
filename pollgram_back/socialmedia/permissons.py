from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS and not obj.is_superuser:
            return True
        elif request.user == obj:
            return True
        else:
            return False