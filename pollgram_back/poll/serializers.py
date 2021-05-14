from rest_framework import serializers

from poll.models import Poll, Choice, Vote
from socialmedia.serializers.user import UserSummarySerializer


class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(source='get_votes.count', read_only=True)
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('id', 'order', 'context', 'poll', 'vote_count')
        read_only_fields = ('id',)


class PollSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable')
        read_only_fields = ('id',)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data, creator=self.context['request'].user)
        # todo save all choices in one request
        for choice in choices:
            Choice.objects.create(poll=poll, **choice)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    selected = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('user', 'id', 'selected')
        read_only_fields = ('id',)
