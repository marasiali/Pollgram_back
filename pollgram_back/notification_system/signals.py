from socialmedia.models import FollowRelationship
from poll.models import Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

@receiver(post_save, sender=FollowRelationship)
def notify_follow_relationship(sender, instance, created, **kwargs):
    if created:
        if instance.pending:
            notify.send(
                sender=instance.from_user,
                recipient=instance.to_user,
                verb="follow-request",
            )
        else:
            notify.send(
                sender=instance.from_user,
                recipient=instance.to_user,
                verb="follow",
            )
    else:
        if not instance.pending:
            notify.send(
                sender=instance.to_user,
                recipient=instance.from_user,
                verb="follow-accept",
            )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        poll = instance.poll
        if instance.parent:
            notify.send(
                sender=instance.creator,
                recipient=instance.parent.creator,
                verb="reply-on-your-comment",
                action_object=instance,
                target=poll
            )
            notify.send(
                sender=instance.creator,
                recipient=poll.creator,
                verb="reply-on-your-poll",
                action_object=instance,
                target=poll
            )
        else:
            notify.send(
                sender=instance.creator,
                recipient=poll.creator,
                verb="comment",
                action_object=instance,
                target=poll
            )