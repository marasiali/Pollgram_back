from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Vote, Choice
from .paginations import PollPagination
from .permissions import IsCreatorOrReadOnly
from .serializers import PollSerializer, VoteSerializer


class PollRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]


class PollListAPIView(ListAPIView):
    pagination_class = PollPagination
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), id=self.kwargs['pk'])
        return user.polls.all()


class PollCreateAPIView(CreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]


class VoteCreateAPIView(APIView):
    def post(self, request, pk):
        Vote.objects.create(user=request.user, selected=Choice.objects.get(id=pk))
        return Response({
            "status": "voted"
        }, status=status.HTTP_201_CREATED)
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
