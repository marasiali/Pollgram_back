from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.authtoken.admin import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from socialmedia.pagination import SearchResultsSetPagination

from poll.models import Poll
from poll.paginations import PollPagination
from poll.serializers import PollRetrieveVisibleSerializer, PollRetrieveInvisibleSerializer
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


class UserTimelineListAPIView(APIView, PollPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followings = self.request.user.get_followings().prefetch_related('polls')
        polls = Poll.objects.none()
        for following in followings:
            polls = polls | following.polls.all()
        polls = polls | self.request.user.polls.all()
        return serialize_polls(polls, self.request.user)


class PollListAPIView(APIView, PollPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), id=pk)
        polls = user.polls.all()
        return serialize_polls(polls, user)


def serialize_polls(polls, user):
    serialized_polls = list()
    for poll in polls:
        visibility_status = poll.visibility_status
        if visibility_status == Poll.PollVisibilityStatus.VISIBLE or (
                visibility_status == Poll.PollVisibilityStatus.VISIBLE_AFTER_VOTE and is_already_voted(poll))\
                or poll.creator == user:
            serialized_polls.append(PollRetrieveVisibleSerializer(poll).data)
        elif visibility_status == Poll.PollVisibilityStatus.HIDDEN or (
                visibility_status == Poll.PollVisibilityStatus.VISIBLE_AFTER_VOTE and not is_already_voted(poll)):
            serialized_polls.append(PollRetrieveInvisibleSerializer(poll).data)
    return Response(serialized_polls, status=status.HTTP_200_OK)


def is_already_voted(poll):
    user = poll.creator
    return poll.choices.filter(votes__user=user).exists()
