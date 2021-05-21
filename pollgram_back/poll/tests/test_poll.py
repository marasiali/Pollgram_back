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
                    "context": "48",
                    "order": "1"
                },
                {
                    "context": "22",
                    "order": "2"
                }
            ]
        }, HTTP_AUTHORIZATION=token, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('how old are you?', response.data['question'])
        self.assertEqual('about age', response.data['description'])
        self.assertEqual(1, response.data['creator']['id'])
        self.assertEqual('ali', response.data['creator']['username'])
        self.assertEqual(2, len(response.data['choices']))
        self.assertEqual('48', response.data['choices'][0]['context'])
        self.assertEqual(1, response.data['choices'][0]['order'])
        self.assertEqual('22', response.data['choices'][1]['context'])
        self.assertEqual(2, response.data['choices'][1]['order'])

    def test_get_poll(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, response.data['id'])
        self.assertEqual("what's your favourite car", response.data['question'])
        self.assertEqual('car poll', response.data['description'])
        self.assertEqual(2, response.data['creator']['id'])
        self.assertEqual('sadra', response.data['creator']['username'])
        self.assertEqual(3, len(response.data['choices']))

    def test_delete_poll_not_creator_user(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(Poll.objects.filter(id=3).exists())

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
        response = self.client.post('/api/poll/vote/1/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(vote_count_before + 1, Choice.objects.get(id=2).votes.count())
        print(response.data)
        self.assertEqual(2, response.data['orders'][0])
        self.assertEqual(2, response.data['user'])

    def test_vote_already_voted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        self.client.post('/api/poll/vote/1/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        vote_count_before = Choice.objects.get(id=2).votes.count()
        response = self.client.post('/api/poll/vote/1/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(vote_count_before, Choice.objects.get(id=2).votes.count())
