from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class User(AbstractUser):

    def uploadAvatar(instance, filename):
        username = instance.username
        ext = filename.split('.')[-1]
        formatted_time = timezone.localtime(timezone.now()).strftime('%Y%m%d%H%M%S')
        return f'profile/avatar/{username}{formatted_time}.{ext}'

    def uploadCover(instance, filename):
        ext = filename.split('.')[-1]
        username = instance.username
        formatted_time = timezone.localtime(timezone.now()).strftime('%Y%m%d%H%M%S')
        return f'profile/cover/{username}{formatted_time}.{ext}'

    # TODO: default avatar image?
    # TODO: resize images before save and probably save a thumbnail copy
    avatar = models.ImageField("Avatar", blank=True, null=True, upload_to=uploadAvatar)
    cover = models.ImageField("Cover", blank=True, null=True, upload_to=uploadCover)
    bio = models.CharField("Bio", blank=True, max_length=220)
    is_public = models.BooleanField("IsPublic?", default=True)
    is_verified = models.BooleanField("Verified?", default=False)
    followings = models.ManyToManyField("self", related_name='followers', symmetrical=False,
                                        through='FollowRelationship')

    def get_followers(self):
        # sort results have added to have a stable response
        return self.followers.filter(follows_relationships__pending=False).order_by('-id')

    def get_followings(self):
        # sort results have added to have a stable response
        return self.followings.filter(followed_relationships__pending=False).order_by('-id')

    def get_follow_status(self, to_user):
        if self == to_user:
            return None
        try:
            follow_rel = FollowRelationship.objects.get(from_user=self, to_user=to_user)
            if follow_rel.pending:
                return 'Pending'
            else:
                return 'Followed'
        except FollowRelationship.DoesNotExist:
            return 'NotFollowed'

    def can_see_poll(self, poll):
        visibility_status = poll.visibility_status
        return visibility_status == 'VI' or (
                visibility_status == 'VA' and
                self.is_already_voted(poll)) or poll.creator == self

    def is_already_voted(self, poll):
        return poll.choices.filter(votes__user=self).exists()

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.username


class FollowRelationship(models.Model):
    from_user = models.ForeignKey(get_user_model(), verbose_name="From", on_delete=models.CASCADE,
                                  related_name="follows_relationships")
    to_user = models.ForeignKey(get_user_model(), verbose_name="To", on_delete=models.CASCADE,
                                related_name="followed_relationships")
    pending = models.BooleanField(verbose_name="IsPending?")

    class Meta:
        verbose_name = "FollowRelationship"
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        # ask for needed test?
        return f"{self.from_user.username} -> {self.to_user.username} {'(pending)' if self.pending else ''}"
