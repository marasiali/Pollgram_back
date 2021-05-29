from rest_framework import serializers
from notifications.models import Notification
from poll.models import Poll, Comment
from socialmedia.models import User
from socialmedia.serializers.user import UserSummarySerializer
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


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


@extend_schema_serializer(
    examples = [
        OpenApiExample(
            'follow',
            summary='Follow',
            description="""
            This notification means somebody followed you. (Your page is public)

            In the response:

                actor           ->    The user who followed you

                action_object   ->    <not-used in this type>

                target          ->    <not-used in this type>
            """,
            value=[
                    {
                        "slug": 110917,
                        "actor": {
                            "id": 1,
                            "username": "admin",
                            "first_name": "",
                            "last_name": "",
                            "avatar": None,
                            "bio": "",
                            "is_public": True,
                            "is_verified": False
                        },
                        "action": "follow",
                        "action_object": None,
                        "target": None,
                        "unread": True,
                        "timestamp": "2021-05-29T16:52:44.364916+04:30"
                    }
                ],
        ),
        OpenApiExample(
            'follow-request',
            summary='FollowRequest',
            description="""
            This notification means somebody reqested to follow you. (Your page is private)

            In the response:

                actor           ->    The user who requested to follow you

                action_object   ->    <not-used in this type>

                target          ->    <not-used in this type>
            """,
            value=[
                    {
                        "slug": 110918,
                        "actor": {
                            "id": 3,
                            "username": "user3",
                            "first_name": "user3",
                            "last_name": "third",
                            "avatar": None,
                            "bio": "",
                            "is_public": True,
                            "is_verified": False
                        },
                        "action": "follow-request",
                        "action_object": None,
                        "target": None,
                        "unread": True,
                        "timestamp": "2021-05-29T16:54:02.169506+04:30"
                    },
                ],
        ),
        OpenApiExample(
            'follow-accept',
            summary='Accept FollowRequest',
            description="""
            This notification means you have already requested a user to follow 
            and he/she has now accepted it.

            In the response:

                actor           ->    The user who accept your follow request

                action_object   ->    <not-used in this type>

                target          ->    <not-used in this type>
            """,
            value=[
                    {
                        "slug": 110920,
                        "actor": {
                            "id": 2,
                            "username": "user2",
                            "first_name": "user",
                            "last_name": "secondary",
                            "avatar": None,
                            "bio": "im' fake 2",
                            "is_public": False,
                            "is_verified": False
                        },
                        "action": "follow-accept",
                        "action_object": None,
                        "target": None,
                        "unread": True,
                        "timestamp": "2021-05-29T16:56:14.267598+04:30"
                    },
                ]
        ),
        OpenApiExample(
            'comment',
            summary='Reply on your comment',
            description="""
            This notification means somebody commented on your poll.

            In the response:

                actor           ->    The user who sent the comment

                action_object   ->    The comment object

                target          ->    Poll obeject of the comment
            """,
            value=[
                    {
                        "slug": 110914,
                        "actor": {
                            "id": 2,
                            "username": "user2",
                            "first_name": "user",
                            "last_name": "secondary",
                            "avatar": None,
                            "bio": "im' fake 2",
                            "is_public": False,
                            "is_verified": False
                        },
                        "action": "comment",
                        "action_object": {
                            "id": 6,
                            "content": "new2 comment from user2",
                            "parent": None
                        },
                        "target": {
                            "id": 2,
                            "question": "question1",
                            "description": "q1 desc",
                            "category": None
                        },
                        "unread": True,
                        "timestamp": "2021-05-29T13:15:29.029214+04:30"
                    },
                ],
        ),
         OpenApiExample(
            'reply-on-your-comment',
            summary='Reply on your comment',
            description="""
            This notification means somebody replied on your comment.

            In the response:

                actor           ->    The user who sent the reply

                action_object   ->    The reply object

                target          ->    Poll obeject of the reply
            """,
            value=[
                    {
                        "slug": 110915,
                        "actor": {
                            "id": 3,
                            "username": "user3",
                            "first_name": "user3",
                            "last_name": "third",
                            "avatar": None,
                            "bio": "",
                            "is_public": True,
                            "is_verified": False
                        },
                        "action": "reply-on-your-comment",
                        "action_object": {
                            "id": 7,
                            "content": "new reply from user3",
                            "parent": 6
                        },
                        "target": {
                            "id": 2,
                            "question": "question1",
                            "description": "q1 desc",
                            "category": None
                        },
                        "unread": True,
                        "timestamp": "2021-05-29T13:30:42.724010+04:30"
                    }
                ],
        ),
        OpenApiExample(
            'reply-on-your-poll',
            summary='Reply on your poll',
            description="""
            This notification means somebody replied on the comment of somebody else,
            in the comments of your poll.

            In the response:

                actor           ->    The user who sent the reply

                action_object   ->    The reply object

                target          ->    Poll obeject of the reply
            """,
            value=[
                    {
                        "slug": 110916,
                        "actor": {
                            "id": 3,
                            "username": "user3",
                            "first_name": "user3",
                            "last_name": "third",
                            "avatar": None,
                            "bio": "",
                            "is_public": True,
                            "is_verified": False
                        },
                        "action": "reply-on-your-poll",
                        "action_object": {
                            "id": 7,
                            "content": "new reply from user3",
                            "parent": 6
                        },
                        "target": {
                            "id": 2,
                            "question": "question1",
                            "description": "q1 desc",
                            "category": None
                        },
                        "unread": True,
                        "timestamp": "2021-05-29T13:30:42.802609+04:30"
                    },
                ],
        ),
    ]
)
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

