from django.db.models.signals import post_save
from django.dispatch import receiver

from socialmedia.models import User, FollowRelationship


@receiver(post_save, sender=User)
def accept_all_follow_requests(sender, instance, created, **kwargs):
    if not created and instance.is_public:
        follow_relationships = FollowRelationship.objects.filter(to_user=instance, pending=True)
        if follow_relationships.exists():
            follow_relationships.update(pending=False)
