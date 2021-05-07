from rest_framework import serializers

from poll.models import Poll, Choice, Vote
from socialmedia.models import User


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'first_name', 'last_name',)
        read_only_fields = ('id', 'avatar',)


class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('id', 'order', 'context', 'poll', 'vote_count')
        read_only_fields = ('id',)

    def get_vote_count(self, obj):
        return obj.votes.count()


class PollSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'created_at', 'question', 'description', 'creator', 'choices',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data, creator=self.context['request'].user)
        # todo save all choices in one request
        for choice in choices:
            Choice.objects.create(poll=poll, **choice)
        return poll

    def to_representation(self, instance):
        representation = super(PollSerializer, self).to_representation(instance)
        return representation


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    selected = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('user', 'id', 'selected')
        read_only_fields = ('id',)
