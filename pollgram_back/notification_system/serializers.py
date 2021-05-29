from rest_framework import serializers
from notifications.models import Notification
from poll.models import Poll, Comment
from socialmedia.models import User
from socialmedia.serializers.user import UserSummarySerializer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'question', 'description','category')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'parent')

class GenericNotificationRelatedField(serializers.RelatedField):
    
    def to_representation(self, instance):
        if isinstance(instance, User):
            return UserSummarySerializer(instance).data
        elif isinstance(instance, Poll):
            return PollSerializer(instance).data
        elif isinstance(instance, Comment):
            return CommentSerializer(instance).data


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSummarySerializer(read_only=True)
    action = serializers.CharField(source='verb', read_only=True)
    action_object = GenericNotificationRelatedField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    class Meta:
        model = Notification
        fields = (
            'slug',
            'actor',
            'action',
            'action_object',
            'target',
            'unread',
            'timestamp',
        )

