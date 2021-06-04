from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class CommentAndReplyTest(APITestCase):
    fixtures = ['users', 'comments']

    def test_comment_on_poll_by_creator_user_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "test private",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test private', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_comment_on_poll_by_other_when_page_is_public(self):
        user = User.objects.get(id=1)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/12/comment/', {
            "content": "test public page",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test public page', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_comment_on_poll_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/21/comment/', {
            "content": "test private page follower",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test private page follower', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_comment_on_poll_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "hello comment",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_comment_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('i like ford', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_get_comment_by_other_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/12/comment/6/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('I am tatality', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_get_comment_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/2/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('i like benz more', response.data['content'])
        self.assertIsNone(response.data['parent'])

    def test_get_comment_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_reply_on_comment_by_creator_user_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "test private",
            "parent": "1"
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test private', response.data['content'])
        self.assertEqual(1, response.data['parent'])

    def test_reply_on_comment_by_other_when_page_is_public(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/12/comment/', {
            "content": "test public page",
            "parent": "6"
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test public page', response.data['content'])
        self.assertEqual(6, response.data['parent'])

    def test_reply_on_comment_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "test private page follower",
            "parent": "1"
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('test private page follower', response.data['content'])
        self.assertEqual(1, response.data['parent'])

    def test_reply_on_comment_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "hello comment",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_reply_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/5/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('I do not give a shit', response.data['content'])
        self.assertEqual(1, response.data['parent'])

    def test_get_reply_by_other_user_when_page_is_public(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/12/comment/8/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Me too', response.data['content'])
        self.assertEqual(6, response.data['parent'])

    def test_get_reply_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/4/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('I hate ford', response.data['content'])
        self.assertEqual(1, response.data['parent'])

    def test_get_reply_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_comments_list_by_creator_user_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(1, data[1]['id'])
        self.assertEqual('i like ford', data[1]['content'])
        self.assertEqual(2, data[0]['id'])
        self.assertEqual('i like benz more', data[0]['content'])

    def test_get_comments_list_by_other_user_when_page_is_public(self):
        user = User.objects.get(id=3)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/12/comment/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(6, data[1]['id'])
        self.assertEqual('I am tatality', data[1]['content'])
        self.assertEqual(7, data[0]['id'])
        self.assertEqual('I love tataloo', data[0]['content'])

    def test_get_comments_list_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(1, data[1]['id'])
        self.assertEqual('i like ford', data[1]['content'])
        self.assertEqual(2, data[0]['id'])
        self.assertEqual('i like benz more', data[0]['content'])

    def test_get_comments_list_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_replies_list_by_creator_user_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/reply/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(4, data[1]['id'])
        self.assertEqual('I hate ford', data[1]['content'])
        self.assertEqual(5, data[0]['id'])
        self.assertEqual('I do not give a shit', data[0]['content'])

    def test_get_replies_list_by_other_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/12/comment/6/reply/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(8, data[1]['id'])
        self.assertEqual('Me too', data[1]['content'])
        self.assertEqual(6, data[1]['parent'])
        self.assertEqual(9, data[0]['id'])
        self.assertEqual('You are idiot', data[0]['content'])
        self.assertEqual(6, data[1]['parent'])

    def test_get_replies_list_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/reply/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data['results']
        self.assertEqual(2, len(data))
        self.assertEqual(4, data[1]['id'])
        self.assertEqual('I hate ford', data[1]['content'])
        self.assertEqual(5, data[0]['id'])
        self.assertEqual('I do not give a shit', data[0]['content'])

    def test_get_replies_list_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/reply/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class LikeAndDislikeTest(APITestCase):
    fixtures = ['users', 'comments']

    def test_like_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/5/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_like_by_other_user_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/12/comment/8/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_like_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/5/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_like_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_like_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_like_by_other_user_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/12/comment/7/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_like_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_like_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_dislike_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_dislike_by_other_user_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/12/comment/8/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_dislike_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_dislike_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_dislike_by_creator_when_page_is_private(self):
        user = User.objects.get(id=6)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/5/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_dislike_by_other_user_user_when_page_is_public(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/12/comment/9/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_dislike_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        user = User.objects.get(id=2)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/5/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_dislike_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
