from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Vote, Image, File
from .permissions import IsCreatorOrReadOnly
from .serializers import PollCreateSerializer, ImageSerializer, FileSerializer, PollRetrieveSerializer, VoteSerializer


class PollRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollRetrieveSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]


class PollCreateAPIView(CreateAPIView):
    model = Poll
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated]


class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_pk):
        user = request.user
        poll = get_object_or_404(Poll, pk=poll_pk)
        if poll.choices.filter(votes__user=user).exists():
            return Response({
                "status": "already voted"
            }, status=status.HTTP_409_CONFLICT)
        choices = poll.choices.filter(order__in=request.data['selected'])
        if len(choices) < poll.min_choice_can_vote or len(choices) > poll.max_choice_can_vote:
            return Response({
                "status": "invalid number of votes"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        created_vote = Vote.objects.create(user=user)
        created_vote.selected.set(choices)
        return Response(VoteSerializer(created_vote).data, status=status.HTTP_201_CREATED)

    def delete(self, request, poll_pk):
        user = request.user
        poll = get_object_or_404(Poll, pk=poll_pk)
        if not poll.choices.filter(votes__user=user).exists():
            return Response({
                "status": "not voted yet"
            }, status=status.HTTP_409_CONFLICT)
        choices = poll.choices.filter(order__in=request.data['selected'])
        Vote.objects.filter(user=user, selected__in=choices).delete()
        return Response({
            "status": "vote retracted"
        }, status=status.HTTP_204_NO_CONTENT)


class ImageCreateAPIView(CreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]


class FileCreateAPIView(CreateAPIView):
    model = File
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
