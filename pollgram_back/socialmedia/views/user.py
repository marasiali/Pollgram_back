from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.authtoken.admin import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .pagination import SearchResultsSetPagination
from ..serializers.user import (
    UserAdminAccessSerializer,
    UserBaseAccessSerializer,
    UserAvatarSerializer,
    UserCoverSerializer, UserSummarySerializer,
)
from ..permissons import IsSelfOrReadOnly

class UserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model()
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

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

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    pagination_class = SearchResultsSetPagination

    serializer_class = UserSummarySerializer
