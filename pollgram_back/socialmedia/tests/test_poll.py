from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class UserPollTest(APITestCase):
    fixtures = ['poll_users_fixture', 'poll_fixture', 'poll_followRelationship_fixture']

    def test_get_user_polls(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/2/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_polls = response.data['results']
        self.assertEqual(7, len(user_polls))
        for poll in user_polls:
            self.assertEqual(2, poll['creator']['id'])

        right_polls_order = [11, 8, 6, 5, 4, 3, 2]
        for i in range(0, 7):
            self.assertEqual(right_polls_order[i], user_polls[i]['id'])

    def test_get_user_timeline(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/timeline/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        polls = response.data['results']
        self.assertEqual(10, len(polls))

        create_times = []
        for poll in polls:
            create_times.append(poll['created_at'])
        self.assertTrue(create_times == sorted(create_times, reverse=True))

        right_polls_order = [12, 11, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(0, 10):
            self.assertEqual(right_polls_order[i], polls[i]['id'])
