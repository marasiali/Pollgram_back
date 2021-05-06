from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ..models import FollowRelationship
from ..permissons import IsSelfOrReadOnly
from ..serializers.user import UserSummarySerializer


class DefaultPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get(self, request, pk):
        to_user = get_object_or_404(get_user_model(), pk=pk)
        follow_status = request.user.get_follow_status(to_user=to_user)
        return Response({
            "status": follow_status
        })

    def post(self, request, pk):
        to_user = get_object_or_404(get_user_model(), pk=pk)
        if FollowRelationship.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        elif to_user.is_public:
            FollowRelationship.objects.create(
                from_user=request.user, to_user=to_user, pending=False)
            return Response({
                "status": "Followed"
            }, status=status.HTTP_201_CREATED)
        else:
            FollowRelationship.objects.create(
                from_user=request.user, to_user=to_user, pending=True)
            return Response({
                "status": "Pending"
            }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        to_user = get_object_or_404(get_user_model(), pk=pk)
        if not FollowRelationship.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        else:
            FollowRelationship.objects.filter(
                from_user=request.user, to_user=to_user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingsAPIView(ListAPIView):
    serializer_class = UserSummarySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs['pk'])
        return user.get_followings()


class FollowersAPIView(ListAPIView):
    serializer_class = UserSummarySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs['pk'])
        return user.get_followers()
