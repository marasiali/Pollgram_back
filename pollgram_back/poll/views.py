from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from socialmedia.models import User
from .models import Poll, Vote, Image, File, Choice, Category, Comment
from .paginations import VotersPagination, PollPagination, CommentPagination, ReplyPagination
from .permissions import IsCreatorOrReadOnly, IsCreatorOrPublicPoll, CommentFilterPermission, IsFollowerOrPublic, \
    IsFollowerOrPublicForGetAPoll, IsFollowerOrPublicForGetAComment, IsSelf
from .serializers import PollCreateSerializer, ImageSerializer, FileSerializer, \
    VoteResponseSerializer, VoterUserSerializer, PollRetrieveSerializer, CategorySerializer, CommentSerializer, \
    ChoiceSerializer


class PollRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = PollRetrieveSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly, IsFollowerOrPublicForGetAPoll]

    def get_queryset(self):
        return Poll.objects.exclude(creator__blocked_users=self.request.user)


class PollCreateAPIView(CreateAPIView):
    model = Poll
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated]


class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFollowerOrPublic]

    def post(self, request, poll_pk):
        user = request.user
        
        poll = get_object_or_404(Poll, ~Q(creator__blocked_users=request.user), pk=poll_pk)
        if poll.choices.filter(votes__user=user).exists():
            return Response({
                "status": "already voted"
            }, status=status.HTTP_409_CONFLICT)
        choices = poll.choices.filter(order__in=request.data.get('selected', []))
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
        poll = get_object_or_404(Poll, ~Q(creator__blocked_users=request.user), pk=poll_pk)
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
    permission_classes = [IsAuthenticated, IsCreatorOrPublicPoll, IsFollowerOrPublic]
    pagination_class = VotersPagination
    serializer_class = VoterUserSerializer

    def get_queryset(self):
        poll_id = self.kwargs['poll_pk']
        order = self.kwargs['order']
        choice = get_object_or_404(Choice, ~Q(poll__creator__blocked_users=self.request.user), poll=poll_id, order=order)
        user_ids = choice.votes.all().values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids).exclude(blocked_users=self.request.user)


class ImageCreateAPIView(CreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]


class FileCreateAPIView(CreateAPIView):
    model = File
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]


class CategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        main_categories = Category.objects.filter(parent=None)
        return main_categories


class CategoryPollsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PollRetrieveSerializer
    pagination_class = PollPagination

    def get_queryset(self):
        category_id = self.kwargs['cat_pk']
        category = get_object_or_404(Category, id=category_id)
        if category.parent is None:
            sub_categories = category.get_sub_categories().prefetch_related('polls')
            polls = Poll.objects.none()
            for sub_cat in sub_categories:
                polls = polls | sub_cat.polls.filter(creator__is_public=True).exclude(creator__blocked_users=self.request.user)
            return polls | category.polls.filter(creator__is_public=True).exclude(creator__blocked_users=self.request.user)
        else:
            return Poll.objects.filter(category=category, creator__is_public=True).exclude(creator__blocked_users=self.request.user)


class CommentRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly, IsFollowerOrPublicForGetAComment]
    lookup_url_kwarg = "comment_pk"

    def get_queryset(self):
        poll = get_object_or_404(Poll, ~Q(creator__blocked_users=self.request.user), pk=self.kwargs.get('poll_pk'))
        return poll.comments.exclude(creator__blocked_users=self.request.user)


class CommentListCreateAPIView(ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticated, CommentFilterPermission, IsFollowerOrPublic]
    ordering_fields = ['likes', 'dislikes']

    def get_serializer_context(self):
        context = super(CommentListCreateAPIView, self).get_serializer_context()
        context['poll'] = get_object_or_404(Poll, ~Q(creator__blocked_users=self.request.user), pk=self.kwargs.get('poll_pk'))
        return context

    def get_queryset(self):
        filter_order = self.request.query_params.get('order')

        if filter_order:
            poll = get_object_or_404(Poll, ~Q(creator__blocked_users=self.request.user), id=self.kwargs['poll_pk'])
            choice = get_object_or_404(Choice, poll=poll, order=filter_order)
            users = choice.votes.all().values_list('user', flat=True)
            return Comment.objects.filter(creator__in=users, poll=poll).exclude(creator__blocked_users=self.request.user)
        else:
            poll = get_object_or_404(Poll, ~Q(creator__blocked_users=self.request.user), id=self.kwargs['poll_pk'])
            return poll.comments.filter(parent=None).exclude(creator__blocked_users=self.request.user)


class ReplyListAPIView(ListAPIView):
    pagination_class = ReplyPagination
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsFollowerOrPublic]

    def get_queryset(self):
        comment = get_object_or_404(Comment, ~Q(creator__blocked_users=self.request.user), ~Q(poll__creator__blocked_users=self.request.user),\
                                     id=self.kwargs['comment_pk'])
        return comment.replies.all().exclude(creator__blocked_users=self.request.user)


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFollowerOrPublic]

    def post(self, request, poll_pk, comment_pk):
        user = request.user
        comment = get_object_or_404(Comment,  ~Q(creator__blocked_users=request.user), ~Q(poll__creator__blocked_users=request.user),\
                                    pk=comment_pk)
        if comment.likes.filter(pk=user.pk).exists():
            return Response({"msg": "already liked"}, status=status.HTTP_409_CONFLICT)
        if comment.dislikes.filter(pk=user.pk).exists():
            comment.dislikes.remove(user)

        comment.likes.add(user)

        return Response({"msg": "liked"}, status=status.HTTP_201_CREATED)

    def delete(self, request, poll_pk, comment_pk):
        user = request.user
        comment = get_object_or_404(Comment,  ~Q(creator__blocked_users=request.user), ~Q(poll__creator__blocked_users=request.user),\
                                    pk=comment_pk)
        if not comment.likes.filter(pk=user.pk).exists():
            return Response({"msg": "not liked"}, status=status.HTTP_409_CONFLICT)

        comment.likes.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class DislikeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsFollowerOrPublic]

    def post(self, request, poll_pk, comment_pk):
        user = request.user
        comment = get_object_or_404(Comment,  ~Q(creator__blocked_users=request.user), ~Q(poll__creator__blocked_users=request.user),\
                                    pk=comment_pk)
        if comment.dislikes.filter(pk=user.pk).exists():
            return Response({"msg": "already disliked"}, status=status.HTTP_409_CONFLICT)
        if comment.likes.filter(pk=user.pk).exists():
            comment.likes.remove(user)

        comment.dislikes.add(user)

        return Response({"msg": "disliked"}, status=status.HTTP_201_CREATED)

    def delete(self, request, poll_pk, comment_pk):
        user = request.user
        comment = get_object_or_404(Comment,  ~Q(creator__blocked_users=request.user), ~Q(poll__creator__blocked_users=request.user),\
                                    pk=comment_pk)
        if not comment.dislikes.filter(pk=user.pk).exists():
            return Response({"msg": "not disliked"}, status=status.HTTP_409_CONFLICT)

        comment.dislikes.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CircularChartAPIView(ListAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get('poll_pk'))
        return poll.choices

