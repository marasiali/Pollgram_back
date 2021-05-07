from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserAdminAccessSerializer(serializers.ModelSerializer):

    def get_follow_status(self, to_user):
        loggedin_user = self.context['request'].user
        return loggedin_user.get_follow_status(to_user=to_user)

    follow_status = serializers.SerializerMethodField('get_follow_status')
    followers_count = serializers.IntegerField(source='get_followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='get_followings.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'cover',
            'bio',
            'is_public',
            'is_verified',
            'follow_status',
            'followers_count',
            'followings_count',
        )
        read_only_fields = ('id', 'avatar', 'cover',)


class UserBaseAccessSerializer(serializers.ModelSerializer):

    def get_follow_status(self, to_user):
        loggedin_user = self.context['request'].user
        return loggedin_user.get_follow_status(to_user=to_user)

    follow_status = serializers.SerializerMethodField('get_follow_status')
    followers_count = serializers.IntegerField(source='get_followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='get_followings.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'cover',
            'bio',
            'is_public',
            'is_verified',
            'follow_status',
            'followers_count',
            'followings_count',
        )
        read_only_fields = ('id', 'avatar', 'cover', 'email', 'is_verified',)


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar']


class UserCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['cover']


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_public',
            'is_verified',
        )
        read_only_fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_public',
            'is_verified',
        )
