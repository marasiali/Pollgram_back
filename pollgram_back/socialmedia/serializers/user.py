from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserAdminAccessSerializer(serializers.ModelSerializer):
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
            'followers_count',
            'followings_count',
        )
        read_only_fields = ('id', 'avatar', 'cover',)
        
class UserBaseAccessSerializer(serializers.ModelSerializer):
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