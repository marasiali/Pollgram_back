from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile, FollowRelationship

class UserProfileTest(TestCase):

    def test_automatic_create_and_delete_user_profile(self):
        User = get_user_model()
        sample_user = User.objects.create(username='ali', email='ali@test.local', password='12345678')
        self.assertIsNotNone(sample_user.profile)
        sample_user.delete()
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_get_followers(self):
        User = get_user_model()
        sample_user1 = User.objects.create(username='ali', email='ali@test.local', password='12345678')
        sample_user2 = User.objects.create(username='reza', email='reza@test.local', password='12345678')

        # make sure get_followers return empty before make any relation
        self.assertFalse(sample_user1.profile.get_followers().exists())
        self.assertFalse(sample_user2.profile.get_followers().exists())

        # make sure get_followers ignore pending relations
        relation = FollowRelationship.objects.create(from_user=sample_user1.profile, to_user=sample_user2.profile, pending=True)
        self.assertFalse(sample_user1.profile.get_followers().exists())
        self.assertFalse(sample_user2.profile.get_followers().exists())

        # make sure get_followers consider user1 as follower of user2, not vice versa
        relation.pending = False
        relation.save()
        self.assertFalse(sample_user1.profile.get_followers().exists())
        self.assertTrue(sample_user2.profile.get_followers().exists())

    def test_get_followings(self):
        User = get_user_model()
        sample_user1 = User.objects.create(username='ali', email='ali@test.local', password='12345678')
        sample_user2 = User.objects.create(username='reza', email='reza@test.local', password='12345678')

        # make sure get_followings return empty before make any relation
        self.assertFalse(sample_user1.profile.get_followings().exists())
        self.assertFalse(sample_user2.profile.get_followings().exists())

        # make sure get_followings ignore pending relations
        relation = FollowRelationship.objects.create(from_user=sample_user1.profile, to_user=sample_user2.profile, pending=True)
        self.assertFalse(sample_user1.profile.get_followings().exists())
        self.assertFalse(sample_user2.profile.get_followings().exists())

        # make sure get_followings consider user1 as follower of user2, not vice versa
        relation.pending = False
        relation.save()
        self.assertTrue(sample_user1.profile.get_followings().exists())
        self.assertFalse(sample_user2.profile.get_followings().exists())