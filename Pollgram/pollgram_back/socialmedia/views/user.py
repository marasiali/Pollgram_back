from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import (
    UserAdminAccessSerializer,
    UserBaseAccessSerializer,
    UserAvatarSerializer,
    UserCoverSerializer,
)
from ..permissons import IsSelfOrReadOnly


class UserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model()
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'User__first_name', 'User__last_name']

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserAdminAccessSerializer
        else:
            return UserBaseAccessSerializer


class UserAvatarAPIView(RetrieveUpdateAPIView):
    queryset = get_user_model()
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]


class UserCoverAPIView(RetrieveUpdateAPIView):
    queryset = get_user_model()
    serializer_class = UserCoverSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]
