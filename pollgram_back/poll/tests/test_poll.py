from rest_framework import status
from rest_framework.generics import get_object_or_404
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
        data = response.data
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('how old are you?', data['question'])
        self.assertEqual('about age', data['description'])
        self.assertEqual(1, data['creator']['id'])
        self.assertEqual('mehdi', data['creator']['username'])
        self.assertEqual(2, len(data['choices']))
        self.assertEqual('48', data['choices'][0]['context'])
        self.assertEqual(1, data['choices'][0]['order'])
        self.assertEqual('22', data['choices'][1]['context'])
        self.assertEqual(2, data['choices'][1]['order'])

        self.assertTrue(data['is_public'])
        self.assertTrue(data['is_commentable'])
        self.assertTrue(data['is_vote_retractable'])
        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['image'])
        self.assertIsNone(data['file'])
        self.assertEqual(1, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertEqual('VA', data['visibility_status'])

    def test_get_visible_poll(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/3/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, data['id'])
        self.assertEqual('test qu 3', data['question'])
        self.assertEqual('test des 3', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])
        self.assertEqual(4, len(data['choices']))
        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertIsNone(data['image'])
        self.assertEqual('VI', data['visibility_status'])
        self.assertEqual(3, data['max_choice_can_vote'])
        self.assertEqual(2, data['min_choice_can_vote'])
        self.assertFalse(data['is_commentable'])
        self.assertFalse(data['is_public'])
        self.assertFalse(data['is_vote_retractable'])

    def test_get_hidden_poll(self):
        pass
    def test_get_visible_after_vote_poll_when_not_voted(self):
        pass
    def test_get_visible_after_vote_poll_when_voted(self):
        pass


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
        votes = [2]
        response = self.client.post('/api/poll/9/vote/', {
            "selected": votes
        }, format='json', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(votes, list(data['selected']))
        # choice = get_object_or_404(Choice, )


    def test_vote_count(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        vote_count_before = Choice.objects.get(id=28).votes.count()
        response = self.client.post('/api/poll/9/vote/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, response.data['selected'][0])

    def test_vote_already_voted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        self.client.post('/api/poll/2/vote/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        vote_count_before = Choice.objects.get(id=4).votes.count()
        response = self.client.post('/api/poll/2/vote/', {
            "selected": [2]
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(vote_count_before, Choice.objects.get(id=4).votes.count())

    def vote(self, poll_id, voter_user_id, votes):
        user = User.objects.get(id=voter_user_id)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        self.client.post('/api/poll/vote/' + poll_id + '/', {
            "selected": votes
        }, format='json', HTTP_AUTHORIZATION=token)
