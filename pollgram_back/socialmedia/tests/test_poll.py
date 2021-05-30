from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class UserPollTest(APITestCase):
    fixtures = ['poll_users_fixture', 'poll_fixture']

    def test_get_public_page_polls(self):
        user = User.objects.get(id=3)
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

    def test_get_private_page_polls_when_not_followed(self):
        # user 3 doesn't follow user 6
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/6/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_private_page_polls_when_follow_request_not_accepted_yet(self):
        # user 2 sent follow request for user 6 but user 6 doesn't accept yet
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/6/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_private_page_polls_when_follow_request_accepted(self):
        # user 1 sent follow request for user 6 and accepted
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/6/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_polls = response.data['results']
        self.assertEqual(2, len(user_polls))
        for poll in user_polls:
            self.assertEqual(6, poll['creator']['id'])

        right_polls_order = [13, 14]
        for i in range(0, 2):
            self.assertEqual(right_polls_order[i], user_polls[i]['id'])

    def test_get_private_page_polls_by_page_owner(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/user/6/polls/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user_polls = response.data['results']
        self.assertEqual(2, len(user_polls))
        for poll in user_polls:
            self.assertEqual(6, poll['creator']['id'])

        right_polls_order = [13, 14]
        for i in range(0, 2):
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
