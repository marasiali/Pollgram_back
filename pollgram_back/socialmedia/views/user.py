from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.authtoken.admin import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from socialmedia.pagination import SearchResultsSetPagination

from poll.models import Poll
from poll.paginations import PollPagination
from poll.serializers import PollRetrieveSerializer
from ..serializers.user import (
    UserAdminAccessSerializer,
    UserBaseAccessSerializer,
    UserAvatarSerializer,
    UserCoverSerializer, UserSummarySerializer,
)
from ..permissons import IsSelfOrReadOnly, IsFollowerOrPublic


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


class UserTimelineListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PollRetrieveSerializer
    pagination_class = PollPagination

    def get_queryset(self):
        followings = self.request.user.get_followings().prefetch_related('polls')
        polls = Poll.objects.none()
        for following in followings:
            polls = polls | following.polls.all()
        return polls | self.request.user.polls.all()


class PollListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsFollowerOrPublic]
    pagination_class = PollPagination
    serializer_class = PollRetrieveSerializer

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), id=self.kwargs['pk'])
        return user.polls.all()
