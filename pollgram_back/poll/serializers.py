from rest_framework import serializers

from poll.models import Poll, Choice, Vote, File, Image
from socialmedia.serializers.user import UserSummarySerializer


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file')
        read_only_fields = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')
        read_only_fields = ('id',)


class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(source='get_votes.count', read_only=True)
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('id', 'order', 'context', 'poll', 'vote_count')
        read_only_fields = ('id',)


class PollCreateSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'link', 'image',
            'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data, creator=self.context['request'].user)
        # todo save all choices in one request
        for choice in choices:
            Choice.objects.create(poll=poll, **choice)
        return poll


class PollRetrieveSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceSerializer(many=True)
    all_votes = serializers.SerializerMethodField('get_all_votes')
    image = ImageSerializer()
    file = FileSerializer()

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'link', 'image',
            'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'all_votes',)
        read_only_fields = ('id',)

    def get_all_votes(self, obj):
        vote_counter = 0
        for choice in obj.choices.all():
            vote_counter += choice.votes.count()
        return vote_counter


class VoteSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('user', 'id', 'selected')
        read_only_fields = ('id',)
