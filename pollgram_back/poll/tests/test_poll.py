from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from poll.models import Poll
from socialmedia.models import User


class PollTest(APITestCase):
    fixtures = ['polls', 'users']

    def vote_api(self, poll_id, token, votes):
        return self.client.post('/api/poll/' + str(poll_id) + '/vote/', {
            "selected": votes
        }, format='json', HTTP_AUTHORIZATION=token)

    def retract_vote_api(self, poll_id, token):
        return self.client.delete('/api/poll/' + str(poll_id) + '/vote/', HTTP_AUTHORIZATION=token)

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
            ],
            "min_choice_can_vote": 1,
            "max_choice_can_vote": 1
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

    def test_create_poll_when_min_choice_can_vote_is_greater_than_max_choice_can_vote(self):
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
            ],
            "min_choice_can_vote": 3,
            "max_choice_can_vote": 1
        }, HTTP_AUTHORIZATION=token, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_poll_when_poll_have_less_than_two_choice(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/', {
            "question": "how old are you?",
            "description": "about age",
            "choices": [
                {
                    "context": "48",
                    "order": "1"
                }
            ],
            "min_choice_can_vote": 1,
            "max_choice_can_vote": 1
        }, HTTP_AUTHORIZATION=token, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_poll_when_poll_have_more_than_ten_choice(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/', {
            "question": "how old are you?",
            "description": "about age",
            "choices": [
                {
                    "context": "48",
                    "order": "1"
                },                {
                    "context": "48",
                    "order": "2"
                },                {
                    "context": "48",
                    "order": "3"
                },                {
                    "context": "48",
                    "order": "4"
                },                {
                    "context": "48",
                    "order": "5"
                },                {
                    "context": "48",
                    "order": "6"
                },                {
                    "context": "48",
                    "order": "7"
                },                {
                    "context": "48",
                    "order": "8"
                },                {
                    "context": "48",
                    "order": "9"
                },                {
                    "context": "48",
                    "order": "10"
                },                {
                    "context": "48",
                    "order": "10"
                }
            ],
            "min_choice_can_vote": 1,
            "max_choice_can_vote": 1
        }, HTTP_AUTHORIZATION=token, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_visible_poll(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/3/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, data['id'])
        self.assertEqual('test qu 3', data['question'])
        self.assertEqual('test des 3', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(4, len(choices))
        for choice in choices:
            self.assertIsNotNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertIsNone(data['image'])
        self.assertEqual('VI', data['visibility_status'])
        self.assertEqual(3, data['max_choice_can_vote'])
        self.assertEqual(2, data['min_choice_can_vote'])
        self.assertFalse(data['is_commentable'])
        self.assertFalse(data['is_public'])
        self.assertFalse(data['is_vote_retractable'])
        self.assertIsNotNone(data['all_votes'])

    def test_get_hidden_poll_by_creator_user(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/5/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, data['id'])
        self.assertEqual('test qu 5', data['question'])
        self.assertEqual('test des 5', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(3, len(choices))
        for choice in choices:
            self.assertIsNotNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertIsNone(data['image'])
        self.assertEqual('HI', data['visibility_status'])
        self.assertEqual(3, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertFalse(data['is_commentable'])
        self.assertFalse(data['is_public'])
        self.assertFalse(data['is_vote_retractable'])
        self.assertIsNotNone(data['all_votes'])

    def test_get_hidden_poll_by_other_user(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/5/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, data['id'])
        self.assertEqual('test qu 5', data['question'])
        self.assertEqual('test des 5', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(3, len(choices))
        for choice in choices:
            self.assertIsNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertIsNone(data['image'])
        self.assertEqual('HI', data['visibility_status'])
        self.assertEqual(3, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertFalse(data['is_commentable'])
        self.assertFalse(data['is_public'])
        self.assertFalse(data['is_vote_retractable'])
        self.assertIsNone(data['all_votes'])

    def test_get_visible_after_vote_poll_by_other_user_when_not_voted(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/11/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(11, data['id'])
        self.assertEqual('test qu 11', data['question'])
        self.assertEqual('test des 11', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(3, len(choices))
        for choice in choices:
            self.assertIsNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertEqual('b9a62df2-1194-47a2-b958-f72893404043', data['image']['id'])
        self.assertEqual('VA', data['visibility_status'])
        self.assertEqual(2, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertTrue(data['is_commentable'])
        self.assertTrue(data['is_public'])
        self.assertTrue(data['is_vote_retractable'])
        self.assertIsNone(data['all_votes'])

    def test_get_visible_after_vote_poll_by_other_user_when_voted(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        self.client.post('/api/poll/11/vote/', {
            "selected": [1]
        }, HTTP_AUTHORIZATION=token)
        response = self.client.get('/api/poll/11/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(11, data['id'])
        self.assertEqual('test qu 11', data['question'])
        self.assertEqual('test des 11', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(3, len(choices))
        for choice in choices:
            self.assertIsNotNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertEqual('b9a62df2-1194-47a2-b958-f72893404043', data['image']['id'])
        self.assertEqual('VA', data['visibility_status'])
        self.assertEqual(2, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertTrue(data['is_commentable'])
        self.assertTrue(data['is_public'])
        self.assertTrue(data['is_vote_retractable'])
        self.assertIsNotNone(data['all_votes'])

    def test_get_visible_after_vote_poll_by_creator_user_when_not_voted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/11/', HTTP_AUTHORIZATION=token)
        data = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(11, data['id'])
        self.assertEqual('test qu 11', data['question'])
        self.assertEqual('test des 11', data['description'])
        self.assertEqual(2, data['creator']['id'])
        self.assertEqual('sadra', data['creator']['username'])

        choices = data['choices']
        self.assertEqual(3, len(choices))
        for choice in choices:
            self.assertIsNotNone(choice['vote_count'])

        self.assertEqual('', data['attached_http_link'])
        self.assertIsNone(data['file'])
        self.assertEqual('b9a62df2-1194-47a2-b958-f72893404043', data['image']['id'])
        self.assertEqual('VA', data['visibility_status'])
        self.assertEqual(2, data['max_choice_can_vote'])
        self.assertEqual(1, data['min_choice_can_vote'])
        self.assertTrue(data['is_commentable'])
        self.assertTrue(data['is_public'])
        self.assertTrue(data['is_vote_retractable'])
        self.assertIsNotNone(data['all_votes'])

    def test_delete_poll_by_other_user(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(Poll.objects.filter(id=3).exists())

    def test_delete_poll_by_creator_user(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Poll.objects.filter(id=3).exists())

    def test_vote_when_poll_not_exists(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.vote_api(poll_id=100, token=token, votes=[1])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_vote_when_user_voted(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.vote_api(poll_id=9, token=token, votes=[1])
        self.assertEqual([1], list(response.data['selected']))
        response_when_vote_again_same_choice = self.vote_api(poll_id=9, token=token, votes=[1])
        data = response_when_vote_again_same_choice.data
        self.assertEqual(status.HTTP_409_CONFLICT, response_when_vote_again_same_choice.status_code)
        self.assertEqual('already voted', data['status'])

        response_when_vote_again_another_choice = self.vote_api(poll_id=9, token=token, votes=[2])
        data = response_when_vote_again_another_choice.data
        self.assertEqual(status.HTTP_409_CONFLICT, response_when_vote_again_another_choice.status_code)
        self.assertEqual('already voted', data['status'])

    def test_vote_when_user_not_voted_yet(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        # in poll with id 9 all choices vote_count are 0 in database
        vote = [2]
        response = self.vote_api(poll_id=9, token=token, votes=vote)
        data = response.data
        self.assertEqual(vote, list(data['selected']))
        get_poll_response = self.client.get('/api/poll/9/', HTTP_AUTHORIZATION=token)
        poll_data = get_poll_response.data
        self.assertEqual(0, poll_data['choices'][0]['vote_count'])
        self.assertEqual(1, poll_data['choices'][1]['vote_count'])
        self.assertEqual(0, poll_data['choices'][2]['vote_count'])

        self.assertEqual(vote, list(poll_data['voted_choices']))

    def test_vote_with_invalid_number_of_votes(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        votes = [2, 3]
        response = self.vote_api(poll_id=9, token=token, votes=votes)
        data = response.data
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)
        self.assertEqual('invalid number of votes', data['status'])

    def test_retract_vote_when_poll_not_exists(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.retract_vote_api(poll_id=100, token=token)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_retract_vote_when_user_not_voted_yet(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        # in poll with id 9 all choices vote_count are 0 in database and no one vote to it
        response = self.retract_vote_api(poll_id=9, token=token)
        data = response.data
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual('not voted yet', data['status'])

    def test_retract_vote_when_poll_is_retractable(self):
        # poll with id 4 is vote retractable
        # user 1 has voted to 1, 2 no one else have voted to this poll
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'

        retract_votes_response = self.retract_vote_api(poll_id=4, token=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, retract_votes_response.status_code)
        get_poll_response = self.client.get('/api/poll/4/', HTTP_AUTHORIZATION=token)
        poll_data = get_poll_response.data
        self.assertIsNone(poll_data['choices'][0]['vote_count'])
        self.assertIsNone(poll_data['choices'][1]['vote_count'])
        self.assertIsNone(poll_data['choices'][2]['vote_count'])
        self.assertIsNone(poll_data['choices'][3]['vote_count'])
        self.assertEqual([], list(poll_data['voted_choices']))

    def test_retract_vote_when_poll_is_not_vote_retractable(self):
        # poll with id 5 is not vote retractable
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'

        retract_vote_response = self.retract_vote_api(poll_id=5, token=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, retract_vote_response.status_code)
        retract_vote_response_data = retract_vote_response.data
        self.assertEqual('this poll is not vote retractable', retract_vote_response_data['status'])

    def test_all_votes_number_in_poll(self):
        # no one votes to poll with id 12 before
        user1 = User.objects.get(id=1)
        user1_token = f'Bearer {str(AccessToken.for_user(user1))}'
        user1_votes = [1, 2, 4]
        user1_vote_response = self.vote_api(poll_id=12, token=user1_token, votes=user1_votes)
        self.assertEqual(status.HTTP_201_CREATED, user1_vote_response.status_code)

        user2 = User.objects.get(id=2)
        user2_token = f'Bearer {str(AccessToken.for_user(user2))}'
        user2_votes = [1, 2]
        user2_vote_response = self.vote_api(poll_id=12, token=user2_token, votes=user2_votes)
        self.assertEqual(status.HTTP_201_CREATED, user2_vote_response.status_code)

        user3 = User.objects.get(id=3)
        user3_token = f'Bearer {str(AccessToken.for_user(user3))}'
        user3_votes = [1, 4]
        user3_vote_response = self.vote_api(poll_id=12, token=user3_token, votes=user3_votes)
        self.assertEqual(status.HTTP_201_CREATED, user3_vote_response.status_code)

        user4 = User.objects.get(id=4)
        user4_token = f'Bearer {str(AccessToken.for_user(user4))}'
        user4_votes = [1, 3]
        user4_vote_response = self.vote_api(poll_id=12, token=user4_token, votes=user4_votes)
        self.assertEqual(status.HTTP_201_CREATED, user4_vote_response.status_code)

        get_poll_response = self.client.get('/api/poll/12/', HTTP_AUTHORIZATION=user1_token)
        self.assertEqual(status.HTTP_200_OK, get_poll_response.status_code)
        poll_data = get_poll_response.data
        self.assertEqual(9, poll_data['all_votes'])

    def test_get_poll_voters_list_when_poll_not_exists(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/100/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_poll_voters_list_when_choice_not_exists(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/6/choice/100/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_poll_voters_list_when_poll_is_public_and_visible(self):
        # poll with id 2 is visible and public
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/2/choice/4/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        results = data['results']
        self.assertEqual(1, len(results))
        self.assertEqual(2, results[0]['id'])

    def test_get_poll_voters_list_by_creator_user_when_poll_is_anonymous(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/5/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        results = data['results']
        self.assertEqual(2, len(results))
        self.assertEqual(2, results[0]['id'])
        self.assertEqual(1, results[1]['id'])

    def test_get_poll_voters_list_by_other_user_when_poll_is_anonymous(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/5/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_poll_voters_list_by_creator_user_when_poll_is_public_and_visible_after_vote_and_not_voted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/6/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        results = data['results']
        self.assertEqual(2, len(results))
        self.assertEqual(2, results[0]['id'])
        self.assertEqual(1, results[1]['id'])

    def test_get_poll_voters_list_by_other_user_when_poll_is_public_and_visible_after_vote_when_not_voted(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/6/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_poll_voters_list_by_other_user_when_poll_is_public_and_visible_after_vote_when_voted(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        vote = [2]
        vote_response = self.vote_api(poll_id=6, token=token, votes=vote)
        self.assertEqual(status.HTTP_201_CREATED, vote_response.status_code)
        get_voters_response = self.client.get('/api/poll/6/choice/2/voters/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, get_voters_response.status_code)

        get_voters_response_results = get_voters_response.data['results']

        self.assertEqual(3, len(get_voters_response_results))
        self.assertEqual(3, get_voters_response_results[0]['id'])
        self.assertEqual(2, get_voters_response_results[1]['id'])
        self.assertEqual(1, get_voters_response_results[2]['id'])

    def test_get_private_page_poll_by_other_user_when_does_not_follow_the_user(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/13/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_private_page_poll_by_other_user_when_follow_request_not_accepted(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/13/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_private_page_poll_by_other_user_when_follow_request_accepted(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/13/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(13, data['id'])

    def test_get_private_page_poll_by_creator(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/13/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(13, data['id'])

    def test_get_public_page_poll(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/2/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])

    def test_get_circle_chart_by_poll_creator(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/7/chart/circle/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data[0]['order'])
        self.assertEqual(2, data[0]['vote_count'])
        self.assertEqual(2, data[1]['order'])
        self.assertEqual(1, data[1]['vote_count'])
        self.assertEqual(3, data[2]['order'])
        self.assertEqual(1, data[2]['vote_count'])

    def test_get_circle_chart_by_other_user(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/7/chart/circle/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_bar_chart_by_poll_creator(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/7/chart/bar/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data

        self.assertEqual('2021-05-27', str(data[0]['created_at']))
        self.assertEqual(0, data[0]['count'])
        self.assertEqual('2021-05-28', str(data[1]['created_at']))
        self.assertEqual(0, data[1]['count'])
        self.assertEqual('2021-05-29', str(data[2]['created_at']))
        self.assertEqual(0, data[2]['count'])
        self.assertEqual('2021-05-30', str(data[3]['created_at']))
        self.assertEqual(0, data[3]['count'])
        self.assertEqual('2021-05-31', str(data[4]['created_at']))
        self.assertEqual(0, data[4]['count'])
        self.assertEqual('2021-06-01', str(data[5]['created_at']))
        self.assertEqual(0, data[5]['count'])
        self.assertEqual('2021-06-02', str(data[6]['created_at']))
        self.assertEqual(0, data[6]['count'])
        self.assertEqual('2021-06-03', str(data[7]['created_at']))
        self.assertEqual(1, data[7]['count'])
        self.assertEqual('2021-06-04', str(data[8]['created_at']))
        self.assertEqual(2, data[8]['count'])
        self.assertEqual('2021-06-05', str(data[9]['created_at']))
        self.assertEqual(0, data[9]['count'])

    def test_get_bar_chart_by_other_user(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/7/chart/bar/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
