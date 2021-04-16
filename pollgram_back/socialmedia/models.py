from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):

    def uploadAvatar(instance, filename):
        username = instance.user.username
        formatted_time = timezone.localtime(timezone.now()).strftime('%Y%m%d%H%M%S')
        return f'{username}{formatted_time}'

    user = models.OneToOneField(
        get_user_model(),
        unique=True,
        null=True,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # TODO: resize images before save and probably save a thumbnail copy
    avatar = models.ImageField("Avatar", blank=True, null=True, upload_to=uploadAvatar)
    bio = models.CharField("Bio", blank=True, max_length=220)
    is_public = models.BooleanField("IsPublic?", default=True)
    is_verified = models.BooleanField("Verified?", default=False)

    def get_followers(self):
        return self.followers.filter(pending=False)

    def get_followings(self):
        return self.followings.filter(pending=False)

    class Meta:
        verbose_name = "UserProfile"

    def __str__(self):
        return self.user.username




@receiver(models.signals.post_save, sender=get_user_model())
def createUserProfile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class FollowRelationship(models.Model):
    from_user = models.ForeignKey(UserProfile(), verbose_name="From", on_delete=models.CASCADE, related_name="followings")
    to_user = models.ForeignKey(UserProfile(), verbose_name="To", on_delete=models.CASCADE, related_name="followers")
    pending = models.BooleanField(verbose_name="IsPending?")

    class Meta:
        verbose_name = "FollowRelationship"
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} {'(pending)' if self.pending else ''}"
