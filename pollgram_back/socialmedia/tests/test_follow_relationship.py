from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from ..models import FollowRelationship


class FollowRelationshipTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(username='ali', email='ali@test.local')
        self.user2 = User.objects.create(username='reza', email='reza@test.local')

    def test_get_followers(self):
        # make sure get_followers return empty before make any relation
        self.assertFalse(self.user1.get_followers().exists())
        self.assertFalse(self.user2.get_followers().exists())

        # make sure get_followers ignore pending relations
        relation = FollowRelationship.objects.create(from_user=self.user1, to_user=self.user2, pending=True)
        self.assertFalse(self.user1.get_followers().exists())
        self.assertFalse(self.user2.get_followers().exists())

        # make sure get_followers consider user1 as follower of user2, not vice versa
        relation.pending = False
        relation.save()
        self.assertFalse(self.user1.get_followers().exists())
        self.assertTrue(self.user2.get_followers().exists())

    def test_get_followings(self):
        # make sure get_followings return empty before make any relation
        self.assertFalse(self.user1.get_followings().exists())
        self.assertFalse(self.user2.get_followings().exists())

        # make sure get_followings ignore pending relations
        relation = FollowRelationship.objects.create(from_user=self.user1, to_user=self.user2, pending=True)
        self.assertFalse(self.user1.get_followings().exists())
        self.assertFalse(self.user2.get_followings().exists())

        # make sure get_followings consider user1 as follower of user2, not vice versa
        relation.pending = False
        relation.save()
        self.assertTrue(self.user1.get_followings().exists())
        self.assertFalse(self.user2.get_followings().exists())


class CreateDeleteFollowRelationshipAPITest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(username='ali', email='ali@test.local', is_public=True)
        self.user1_token = f'Bearer {str(AccessToken.for_user(self.user1))}'
        self.user2 = User.objects.create(username='reza', email='reza@test.local', is_public=True)
        self.user2_token = f'Bearer {str(AccessToken.for_user(self.user2))}'

    def test_follow_api(self):
        response1 = self.client.post('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.data, {
            "status": "Followed"
        })
        relation_exists1 = FollowRelationship.objects.filter(from_user=self.user1, to_user=self.user2, pending=False).exists()
        self.assertTrue(relation_exists1)
        self.assertEqual(FollowRelationship.objects.count(), 1)

        response2 = self.client.post('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        relation_exists2 = FollowRelationship.objects.filter(from_user=self.user1, to_user=self.user2, pending=False).exists()
        self.assertTrue(relation_exists2)
        self.assertEqual(FollowRelationship.objects.count(), 1)

    def test_follow_api_by_self(self):
        response = self.client.post('/api/user/1/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(FollowRelationship.objects.count(), 0)

    def test_unfollow_api(self):
        FollowRelationship.objects.create(from_user=self.user1, to_user=self.user2, pending=False)
        response1 = self.client.delete('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FollowRelationship.objects.count(), 0)

        response2 = self.client.delete('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(FollowRelationship.objects.count(), 0)

    def test_unfollow_api_by_self(self):
        response = self.client.delete('/api/user/1/follow/', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(FollowRelationship.objects.count(), 0)


class RetrieveFollowRelationshipAPITest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(username='ali', email='ali@test.local', is_public=True)
        self.user1_token = f'Bearer {str(AccessToken.for_user(self.user1))}'
        self.user2 = User.objects.create(username='reza', email='reza@test.local', is_public=True)
        self.user2_token = f'Bearer {str(AccessToken.for_user(self.user2))}'
        self.user3 = User.objects.create(username='sadra', email='sadra@test.local', is_public=True)
        self.user3_token = f'Bearer {str(AccessToken.for_user(self.user3))}'
        
        FollowRelationship.objects.create(from_user=self.user1, to_user=self.user2, pending=False)
        FollowRelationship.objects.create(from_user=self.user1, to_user=self.user3, pending=False)
        FollowRelationship.objects.create(from_user=self.user2, to_user=self.user3, pending=False)
        FollowRelationship.objects.create(from_user=self.user3, to_user=self.user1, pending=False)

    def test_follow_status_api(self):
        self_response = self.client.get('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(self_response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(self_response.data, {
            "status": None
        })

        notfollowed_response = self.client.get('/api/user/1/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(notfollowed_response.status_code, status.HTTP_200_OK)
        self.assertEqual(notfollowed_response.data, {
            "status": "NotFollowed"
        })

        followed_response = self.client.get('/api/user/3/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(followed_response.status_code, status.HTTP_200_OK)
        self.assertEqual(followed_response.data, {
            "status": "Followed"
        })

    def test_follow_status_in_user_info_api(self):
        self_response = self.client.get('/api/user/2/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(self_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self_response.data['follow_status'], None)

        notfollowed_response = self.client.get('/api/user/1/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(notfollowed_response.status_code, status.HTTP_200_OK)
        self.assertEqual(notfollowed_response.data['follow_status'], "NotFollowed")

        followed_response = self.client.get('/api/user/3/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(followed_response.status_code, status.HTTP_200_OK)
        self.assertEqual(followed_response.data['follow_status'], "Followed")

    def test_follow_count_in_user_info_api(self):
        response = self.client.get('/api/user/3/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 2)
        self.assertEqual(response.data['followings_count'], 1)
        
    def test_followers_api(self):
        response = self.client.get('/api/user/3/followers/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        followers = list(map(lambda item: item['id'], response.data['results']))
        self.assertEqual(followers, [2, 1])

    def test_followings_api(self):
        response = self.client.get('/api/user/3/followings/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        followings = list(map(lambda item: item['id'], response.data['results']))
        self.assertEqual(followings, [1])