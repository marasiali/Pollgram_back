from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from poll.models import Poll


class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS and ((obj.creator.get_followers()).filter(
                pk=request.user.id).exists() or obj.creator.is_public):
            return True
        elif request.user == obj.creator:
            return True

        else:
            return False


class IsCreatorOrPublicPoll(BasePermission):

    def has_permission(self, request, view):
        poll = get_object_or_404(Poll, pk=view.kwargs['poll_pk'])
        if request.user.is_superuser or poll.creator == request.user:
            return True
        elif poll.is_public and request.user.can_see_results(poll):
            return True
        else:
            return False


class IsFollowerOrPublic(BasePermission):
    def has_permission(self, request, view):
        poll = get_object_or_404(Poll, pk=view.kwargs['poll_pk'])

        if poll.creator.get_followers().filter(
                pk=request.user.id).exists() or request.user == poll.creator or poll.creator.is_public:
            return True
        else:
            return False


class CommentFilterPermission(BasePermission):

    def has_permission(self, request, view):
        filter_order = request.query_params.get('order')
        if filter_order:
            poll = get_object_or_404(Poll, pk=view.kwargs['poll_pk'])
            return request.user.can_see_results(poll) and poll.is_public
        return True
