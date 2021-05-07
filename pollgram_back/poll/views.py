from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Vote, Choice
from .permissions import IsCreatorOrReadOnly
from .serializers import PollSerializer


class PollRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]


class PollCreateAPIView(CreateAPIView):
    model = Poll
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]


class VoteCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user = request.user
        choice = get_object_or_404(Choice, pk=pk)
        poll = choice.poll
        if poll.choices.filter(votes__user=user).exists():
            return Response({
                "status": "already voted"
            }, status=status.HTTP_409_CONFLICT)
        created_vote = Vote.objects.create(user=user, selected=choice)
        return Response({
            "vote_id": created_vote.id,
            "choice_id": created_vote.selected.id,
            "user_id": created_vote.user.id
        }, status=status.HTTP_201_CREATED)
