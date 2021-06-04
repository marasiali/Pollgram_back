from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework import filters
# from rest_framework.authtoken.admin import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from socialmedia.pagination import SearchResultsSetPagination, BlockedUsersPagination

from poll.models import Poll
from poll.paginations import PollPagination
from poll.serializers import PollRetrieveSerializer

from ..models import FollowRelationship
from ..serializers.user import (
    UserAdminAccessSerializer,
    UserBaseAccessSerializer,
    UserAvatarSerializer,
    UserCoverSerializer, UserSummarySerializer,
)
from ..permissons import IsSelfOrReadOnly, IsFollowerOrPublic


class UserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_queryset(self):
        return get_user_model().objects.exclude(blocked_users=self.request.user)
    

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserAdminAccessSerializer
        else:
            return UserBaseAccessSerializer


class UserAvatarAPIView(RetrieveUpdateAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserCoverAPIView(RetrieveUpdateAPIView):
    serializer_class = UserCoverSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSummarySerializer
    pagination_class = SearchResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    def get_queryset(self):
        return get_user_model().objects.exclude(blocked_users=self.request.user)


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
        user = get_object_or_404(get_user_model(), ~Q(blocked_users=self.request.user), id=self.kwargs['pk'])
        return user.polls.all()


class BlockedUsersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = BlockedUsersPagination
    serializer_class = UserSummarySerializer

    def get_queryset(self):
        return self.request.user.blocked_users.all()


class BlockUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = get_object_or_404(get_user_model(), ~Q(blocked_users=self.request.user), pk=pk)
        if request.user.pk == pk:
            return Response({
                "status": "You can't block yourself."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.blocked_users.filter(pk=pk).exists():
            return Response({
                "status": "already blocked"
            }, status=status.HTTP_409_CONFLICT)
        else:
            request.user.blocked_users.add(user)
            FollowRelationship.objects.filter(Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)).delete()
            return Response(UserSummarySerializer(user).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = get_object_or_404(get_user_model(), ~Q(blocked_users=self.request.user), pk=pk)
        if not request.user.blocked_users.filter(pk=pk).exists():
            return Response({
                "status": "already unblocked"
            }, status=status.HTTP_409_CONFLICT)
        else:
            request.user.blocked_users.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)