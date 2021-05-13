from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class UserPollTest(APITestCase):
    fixtures = ['poll_users_fixture', 'poll_fixture']

    def test_get_all_user_polls(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/2/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, response.json()['count'])
        user_polls = response.json()['results']
        for poll in user_polls:
            self.assertEqual(2, poll['creator']['id'])

    def test_get_timeline_owner_user(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/timeline/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, response.json()['count'])
        polls = response.json()['results']
        create_times = []
        for poll in polls:
            create_times.append(poll['created_at'])
        self.assertTrue(create_times == sorted(create_times, reverse=True))
