from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from poll.models import Poll, Choice
from socialmedia.models import User


class PollTest(APITestCase):
    fixtures = ['polls', 'users']

    def test_create_poll(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/', {
            "question": "how old are you?",
            "description": "about age",
            "choices": [
                {
                    "context": 48,
                    "order": 1
                },
                {
                    "context": 22,
                    "order": 2
                }
            ]
        }, HTTP_AUTHORIZATION=token, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('how old are you?', response.json()['question'])
        self.assertEqual('about age', response.json()['description'])
        self.assertEqual(1, response.json()['creator']['id'])
        self.assertEqual('ali', response.json()['creator']['username'])
        self.assertEqual(2, len(response.json()['choices']))
        self.assertEqual('48', response.json()['choices'][0]['context'])
        self.assertEqual(1, response.json()['choices'][0]['order'])
        self.assertEqual('22', response.json()['choices'][1]['context'])
        self.assertEqual(2, response.json()['choices'][1]['order'])

    def test_get_poll(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.json()['id'])
        self.assertEqual("what's your favourite car", response.json()['question'])
        self.assertEqual('car poll', response.json()['description'])
        self.assertEqual(2, response.json()['creator']['id'])
        self.assertEqual('sadra', response.json()['creator']['username'])
        self.assertEqual(3, len(response.json()['choices']))

    def test_delete_poll_not_creator_user(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertIsNotNone(Poll.objects.get(id=3))

    def test_delete_poll_creator_user(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Poll.objects.filter(id=3).exists())

    def test_vote(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        vote_count_before = Choice.objects.get(id=2).votes.count()
        response = self.client.post('/api/poll/vote/2/', format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(vote_count_before + 1, Choice.objects.get(id=2).votes.count())
        self.assertEqual(2, response.json()['choice_id'])
        self.assertEqual(2, response.json()['user_id'])

    def test_vote_already_voted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        self.client.post('/api/poll/vote/2/', format='json', HTTP_AUTHORIZATION=token)
        vote_count_before = Choice.objects.get(id=2).votes.count()
        response = self.client.post('/api/poll/vote/2/', format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(vote_count_before, Choice.objects.get(id=2).votes.count())
