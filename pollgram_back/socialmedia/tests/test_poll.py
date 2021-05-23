from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class UserPollTest(APITestCase):
    fixtures = ['poll_users_fixture', 'poll_fixture']

    def test_get_user_polls(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/2/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(7, response.data['count'])
        user_polls = response.data['results']
        for poll in user_polls:
            self.assertEqual(2, poll['creator']['id'])

    def test_get_user_timeline(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/timeline/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(7, response.data['count'])
        polls = response.data['results']


        create_times = []
        for poll in polls:
            create_times.append(poll['created_at'])
        self.assertTrue(create_times == sorted(create_times, reverse=True))

