from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
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

    def get_followers(self):
        return self.followers.filter(pending=False)

    def get_followings(self):
        return self.followings.filter(pending=False)

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.username

class FollowRelationship(models.Model):
    from_user = models.ForeignKey(get_user_model(), verbose_name="From", on_delete=models.CASCADE, related_name="followings")
    to_user = models.ForeignKey(get_user_model(), verbose_name="To", on_delete=models.CASCADE, related_name="followers")
    pending = models.BooleanField(verbose_name="IsPending?")

    class Meta:
        verbose_name = "FollowRelationship"
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        # ask for needed test?
        return f"{self.from_user.username} -> {self.to_user.username} {'(pending)' if self.pending else ''}"
