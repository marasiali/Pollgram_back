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

    def test_self_follow_status_api(self):
        response = self.client.get('/api/user/2/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, {
            "status": None
        })

    def test_notfollowed_status_api(self):
        response = self.client.get('/api/user/1/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "status": "NotFollowed"
        })

    def test_followed_status_api(self):
        response = self.client.get('/api/user/3/follow/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "status": "Followed"
        })

    def test_self_follow_status_in_user_info_api(self):
        response = self.client.get('/api/user/2/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['follow_status'], None)

    def test_notfollowed_status_in_user_info_api(self):
        response = self.client.get('/api/user/1/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['follow_status'], "NotFollowed")

    def test_followed_status_in_user_info_api(self):
        response = self.client.get('/api/user/3/', HTTP_AUTHORIZATION=self.user2_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['follow_status'], "Followed")

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


class FollowRequestStatusHandlerAPIViewTest(APITestCase):
    fixtures = ['user_fixture']

    def test_accept_follow_relationship_when_not_exists(self):
        user = get_user_model().objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/user/100/follow-request-status/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_accept_follow_request(self):
        # user 2 follow request for user 4 is pending
        user = get_user_model().objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/user/2/follow-request-status/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        follow_relationship = FollowRelationship.objects.filter(from_user=2, to_user=user.id)
        self.assertEqual('accepted', response.data['status'])
        self.assertFalse(follow_relationship[0].pending)

    def test_reject_follow_request_when_not_exists(self):
        user = get_user_model().objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/user/100/follow-request-status/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_reject_follow_request(self):
        # user 3 follow request for user 4 is pending
        user = get_user_model().objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/user/3/follow-request-status/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        follow_relationship = FollowRelationship.objects.filter(from_user=3, to_user=user.id)
        self.assertFalse(follow_relationship.exists())
