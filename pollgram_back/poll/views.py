from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from socialmedia.models import User
from .models import Poll, Vote, Image, File, Choice
from .permissions import IsCreatorOrReadOnly
from .serializers import PollCreateSerializer, ImageSerializer, FileSerializer, PollRetrieveVisibleSerializer, \
    VoteSerializer, PollRetrieveInvisibleSerializer, VoterUserSerializer


class PollRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    visible_poll_serializer_class = PollRetrieveVisibleSerializer
    invisible_poll_serializer_class = PollRetrieveInvisibleSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def get_serializer_class(self):
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        visibility_status = poll.visibility_status
        if visibility_status == Poll.PollVisibilityStatus.VISIBLE or (
                visibility_status == Poll.PollVisibilityStatus.VISIBLE_AFTER_VOTE and self.is_already_voted()):
            return self.visible_poll_serializer_class
        elif visibility_status == Poll.PollVisibilityStatus.HIDDEN or (
                visibility_status == Poll.PollVisibilityStatus.VISIBLE_AFTER_VOTE and not self.is_already_voted()):
            return self.invisible_poll_serializer_class
        else:
            return Response({
                "status": "unknown poll visibility status"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def is_already_voted(self):
        user = self.request.user
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        return poll.choices.filter(votes__user=user).exists()


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
            }, status=status.HTTP_409_CONFLICT)


class VotersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, poll_pk, order):
        poll = get_object_or_404(Poll, pk=poll_pk)
        choice = get_object_or_404(Choice, poll=poll, order=order)
        print(choice)

        if poll.is_public:
            if poll.visibility_status == Poll.PollVisibilityStatus.VISIBLE or (
                    poll.visibility_status == Poll.PollVisibilityStatus.VISIBLE_AFTER_VOTE and poll.choices.filter(
                    votes__user=request.user).exists()):
                user_ids = choice.votes.all().values_list('user', flat=True)
                users = User.objects.filter(id__in=user_ids)
                return Response(VoterUserSerializer(users, many=True).data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "result is hidden"
                })
        else:
            return Response({
                "status": "poll is not public"
            }, status=status.HTTP_409_CONFLICT)


class ImageCreateAPIView(CreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]


class FileCreateAPIView(CreateAPIView):
    model = File
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
