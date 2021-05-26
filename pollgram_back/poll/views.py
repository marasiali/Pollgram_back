from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from socialmedia.models import User
from .models import Poll, Vote, Image, File, Choice
from .paginations import VotersPagination
from .permissions import IsCreatorOrReadOnly, IsCreatorOrPublicPoll
from .serializers import PollCreateSerializer, ImageSerializer, FileSerializer, \
    VoteResponseSerializer, VoterUserSerializer, PollRetrieveSerializer


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
        choices = poll.choices.filter(order__in=request.data.get('selected'))
        if not choices:
            return Response({
                "selected": "this field is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(choices) < poll.min_choice_can_vote or len(choices) > poll.max_choice_can_vote:
            return Response({
                "status": "invalid number of votes"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        created_vote = Vote.objects.create(user=user)
        created_vote.selected.set(choices)
        return Response(VoteResponseSerializer(created_vote).data, status=status.HTTP_201_CREATED)

    def delete(self, request, poll_pk):
        user = request.user
        poll = get_object_or_404(Poll, pk=poll_pk)
        if poll.is_vote_retractable:
            if not poll.choices.filter(votes__user=user).exists():
                return Response({
                    "status": "not voted yet"
                }, status=status.HTTP_409_CONFLICT)
            choices = poll.choices.all()
            Vote.objects.filter(user=user, selected__in=choices).delete()
            return Response({
                "status": "vote retracted"
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "status": "this poll is not vote retractable"
            }, status=status.HTTP_403_FORBIDDEN)


class VotersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsCreatorOrPublicPoll]
    pagination_class = VotersPagination
    serializer_class = VoterUserSerializer

    def get_queryset(self):
        poll_id = self.kwargs['poll_pk']
        order = self.kwargs['order']
        choice = get_object_or_404(Choice, poll=poll_id, order=order)
        user_ids = choice.votes.all().values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)


class ImageCreateAPIView(CreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]


class FileCreateAPIView(CreateAPIView):
    model = File
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
