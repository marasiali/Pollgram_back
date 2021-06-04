from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from poll.models import Poll, Choice, Vote, File, Image, Category, Comment
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


class PollCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


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

    class Meta:
        model = Choice
        fields = ('order', 'context', 'vote_count')

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

    def validate(self, data):
        if data['min_choice_can_vote'] > data['max_choice_can_vote']:
            raise ValidationError('min_choice_can_vote can not be greater than max_choice_can_vote')
        if not (2 <= len(data['choices']) <= 10):
            raise ValidationError('you can not create poll with less than 2 choices')
        return data


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
    category = PollCategorySerializer()

    class Meta:
        model = Poll
        fields = (
            'id', 'created_at', 'question', 'description', 'creator', 'choices', 'is_commentable', 'attached_http_link',
            'image', 'file', 'max_choice_can_vote', 'min_choice_can_vote', 'is_vote_retractable', 'all_votes',
            'is_public', 'visibility_status', 'voted_choices', 'category')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super(PollRetrieveSerializer, self).to_representation(instance)
        data['voted_choices'] = self.get_user_voted_choices(instance)
        if self.context['request'].user.can_see_results(instance):
            data['all_votes'] = self.get_all_votes(instance)
        return data

    def get_all_votes(self, obj):
        vote_counter = 0
        for choice in obj.choices.all():
            vote_counter += choice.votes.count()
        return vote_counter

    def get_user_voted_choices(self, obj):
        user = self.context['request'].user
        voted_choice_ids = obj.choices.filter(votes__user=user).values_list('order', flat=True)
        return voted_choice_ids


class CommentSerializer(serializers.ModelSerializer):
    creator = UserSummarySerializer(read_only=True)

    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    has_reply = serializers.SerializerMethodField('comment_has_reply')
    like_status = serializers.SerializerMethodField('get_like_status')

    def comment_has_reply(self, obj):
        if obj.replies.count() == 0:
            return False
        return True

    def get_like_status(self, obj):
        user = self.context['request'].user
        if obj.likes.filter(pk=user.pk).exists():
            return 'liked'
        elif obj.dislikes.filter(pk=user.pk).exists():
            return 'disliked'
        else:
            return None

    class Meta:
        model = Comment
        fields = (
            'id', 'created_at', 'content', 'creator', 'parent', 'likes_count', 'dislikes_count', 'poll', 'has_reply',
            'like_status')
        read_only_fields = ('id', 'poll', 'has_reply', 'like_status')

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['poll'] = self.context['poll']
        return super(CommentSerializer, self).create(validated_data)

    def validate(self, data):
        data = super(CommentSerializer, self).validate(data)
        poll = self.context['poll']
        parent = data['parent']

        if not poll.is_commentable:
            raise serializers.ValidationError("The poll is not commentable.")
        if parent and parent.parent:
            raise serializers.ValidationError("You can't reply this comment.")
        if parent and not parent.poll == poll:
            raise serializers.ValidationError("The comment parent doesn't belong to this poll.")
        if parent and parent.creator.blocked_users.filter(pk=self.context['request'].user.pk):
            raise Http404()
        return data


class BarChartSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='created_at')
    count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = Vote
        fields = ('date', 'count')

    def get_count(self, obj):
        return obj['count']
