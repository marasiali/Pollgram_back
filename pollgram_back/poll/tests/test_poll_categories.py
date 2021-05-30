from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class TestCategories(APITestCase):
    fixtures = ['poll_categories', 'users']

    def test_create_poll_with_category(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/', {
            "question": "how old are you?",
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
            "category": "1"
        }, HTTP_AUTHORIZATION=token, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data = response.data
        self.assertEqual(1, data['category'])

    def test_create_poll_with_no_category(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/', {
            "question": "how old are you?",
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
            "category": None
        }, HTTP_AUTHORIZATION=token, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data = response.data
        self.assertIsNone(data['category'])

    def test_get_main_category_polls_when_does_not_have_sub_category(self):
        # poll with id 21 belongs to a private page and main category. it doesn't exist in the response
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/category/4/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(1, len(data))
        self.assertEqual(4, data[0]['category']['id'])
        self.assertEqual('digital', data[0]['category']['name'])

    def test_get_main_category_polls_when_has_sub_category(self):
        # poll 22 and 23 belong to private page, they don't exist in the response
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/category/1/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(4, len(data))
        right_category_id_for_these_polls = [1, 2, 3]
        for poll in data:
            self.assertTrue(poll['category']['id'] in right_category_id_for_these_polls)

    def test_get_sub_category_polls(self):
        # category 3 is category 1 sub category
        # poll with id 23 belongs to a private page and sub category. it doesn't exist in the response

        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/category/3/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(3, data[0]['category']['id'])
        self.assertEqual('programming', data[0]['category']['name'])
        self.assertEqual(3, data[1]['category']['id'])
        self.assertEqual('programming', data[1]['category']['name'])

    def test_get_categories(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/category/', HTTP_AUTHORIZATION=token)
        categories = response.data
        self.assertEqual(2, len(categories))

        self.assertEqual('learning', categories[0]['name'])
        self.assertEqual(1, categories[0]['id'])
        self.assertEqual(1, categories[0]['order'])
        self.assertEqual('digital', categories[1]['name'])
        self.assertEqual(4, categories[1]['id'])
        self.assertEqual(4, categories[1]['order'])

        first_category_sub_categories = categories[0]['sub_categories']
        self.assertEqual('language', first_category_sub_categories[0]['name'])
        self.assertEqual(2, first_category_sub_categories[0]['id'])
        self.assertEqual(2, first_category_sub_categories[0]['order'])

        self.assertEqual('programming', first_category_sub_categories[1]['name'])
        self.assertEqual(3, first_category_sub_categories[1]['id'])
        self.assertEqual(3, first_category_sub_categories[1]['order'])
