from rest_framework import serializers

from poll.models import Poll, Choice, Vote, File, Image, Category
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


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'order')


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField('get_sub_categories')

    class Meta:
        model = Category
        fields = ('id', 'name', 'order', 'sub_categories')

    def get_sub_categories(self, obj):
        return SubCategorySerializer(obj.get_sub_categories(), many=True).data


class ChoiceSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(default=None, read_only=True)
    poll = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('order', 'context', 'poll', 'vote_count')

    def to_representation(self, instance):
        data = super(ChoiceSerializer, self).to_representation(instance)
        if self.context['request'].user.can_see_results(instance.poll):
            data['vote_count'] = instance.get_votes().count()
        return data


class PollCreateSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'min_choice_can_vote', 'max_choice_can_vote', 'is_vote_retractable', 'is_public',
            'visibility_status', 'category')
        read_only_fields = ('id',)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data, creator=self.context['request'].user)
        # todo save all choices in one request
        for choice in choices:
            Choice.objects.create(poll=poll, **choice)
        return poll


class VoteResponseSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField('get_selected_votes')

    class Meta:
        model = Vote
        fields = ('selected',)

    def get_selected_votes(self, obj):
        voted_orders = obj.selected.all().values_list('order', flat=True)
        return voted_orders


class VoterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')
        read_only_fields = ('id', 'avatar')


class PollRetrieveSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)
    choices = ChoiceSerializer(many=True)
    all_votes = serializers.IntegerField(default=None)
    image = ImageSerializer()
    file = FileSerializer()
    voted_choices = serializers.ListField(default=[])

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'all_votes',
            'is_public', 'visibility_status', 'voted_choices', 'category')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super(PollRetrieveSerializer, self).to_representation(instance)
        self.context['request'].path.split()
        if self.context['request'].user.can_see_results(instance):
            data['all_votes'] = self.get_all_votes(instance)
            data['voted_choices'] = self.get_user_voted_choices(instance)
        return data

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
