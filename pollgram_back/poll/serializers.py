from rest_framework import serializers

from poll.models import Poll, Choice, Vote, File, Image
from socialmedia.models import User
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


class ChoiceVisibleCountSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(source='get_votes.count', read_only=True)
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('order', 'context', 'poll', 'vote_count')


class ChoiceInvisibleCountSerializer(serializers.ModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('order', 'context', 'poll',)


class PollCreateSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceVisibleCountSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'is_public',
            'visibility_status')
        read_only_fields = ('id',)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data, creator=self.context['request'].user)
        # todo save all choices in one request
        for choice in choices:
            Choice.objects.create(poll=poll, **choice)
        return poll


class PollRetrieveVisibleSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceVisibleCountSerializer(many=True)
    all_votes = serializers.SerializerMethodField('get_all_votes')
    image = ImageSerializer()
    file = FileSerializer()
    voted_choices = serializers.SerializerMethodField('get_user_voted_choices')

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'all_votes',
            'is_public', 'visibility_status', 'voted_choices')
        read_only_fields = ('id',)

    def get_all_votes(self, obj):
        vote_counter = 0
        for choice in obj.choices.all():
            vote_counter += choice.votes.count()
        return vote_counter

    def get_user_voted_choices(self, obj):
        if hasattr(self.context, 'request'):
            user = self.context['request'].user
        else:
            user = obj.creator
        voted_choice_ids = obj.choices.filter(votes__user=user).values_list('order', flat=True)
        return voted_choice_ids


class PollRetrieveInvisibleSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceInvisibleCountSerializer(many=True)
    image = ImageSerializer()
    file = FileSerializer()

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'is_public',
            'visibility_status')
        read_only_fields = ('id',)


class VoteSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField('get_voted_orders')

    class Meta:
        model = Vote
        fields = ('user', 'id', 'orders')
        read_only_fields = ('id',)

    def get_voted_orders(self, obj):
        voted_orders = obj.selected.all().values_list('order', flat=True)
        return voted_orders


class VoterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')
        read_only_fields = ('id', 'avatar')
