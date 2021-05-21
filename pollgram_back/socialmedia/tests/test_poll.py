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
        self.assertEqual(2, response.data['count'])
        user_polls = response.data['results']
        for poll in user_polls:
            self.assertEqual(2, poll['creator']['id'])

    def test_get_user_timeline(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/timeline/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, response.data['count'])
        polls = response.data['results']
        self.assertEqual(5, polls[0]['id'])
        self.assertEqual(1, polls[0]['creator']['id'])
        self.assertEqual(4, polls[1]['id'])
        self.assertEqual(2, polls[1]['creator']['id'])
        self.assertEqual(3, polls[2]['id'])
        self.assertEqual(2, polls[2]['creator']['id'])
        self.assertEqual(2, polls[3]['id'])
        self.assertEqual(1, polls[3]['creator']['id'])
        self.assertEqual(1, polls[4]['id'])
        self.assertEqual(1, polls[4]['creator']['id'])

        create_times = []
        for poll in polls:
            create_times.append(poll['created_at'])
        self.assertTrue(create_times == sorted(create_times, reverse=True))

