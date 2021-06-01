from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from socialmedia.models import User


class CommentAndReplyTest(APITestCase):
    fixtures = ['users', 'comments']

    def test_comment_on_poll_by_creator_user_when_page_is_private(self):
        pass

    def test_comment_on_poll_by_other_when_page_is_public(self):
        pass

    def test_comment_on_poll_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_comment_on_poll_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/', {
            "content": "hello comment",
            "parent": None
        }, format='json', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_comment_by_creator_when_page_is_private(self):
        pass

    def test_get_comment_by_other_user_when_page_is_public(self):
        pass

    def test_get_comment_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_get_comment_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_comments_list_by_creator_user_when_page_is_private(self):
        pass

    def test_get_comments_list_by_other_user_when_page_is_public(self):
        pass

    def test_get_comments_list_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_get_comments_list_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_replies_list_by_creator_user_when_page_is_private(self):
        pass

    def test_get_replies_list_by_other_user_when_page_is_public(self):
        pass

    def test_get_replies_list_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_get_replies_list_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.get('/api/poll/22/comment/1/reply/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class LikeAndDislikeTest(APITestCase):
    fixtures = ['users', 'comments']

    def test_like_by_creator_when_page_is_private(self):
        pass

    def test_like_by_other_user_user_when_page_is_public(self):
        pass

    def test_like_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_like_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_like_by_creator_when_page_is_private(self):
        pass

    def test_delete_like_by_other_user_user_when_page_is_public(self):
        pass

    def test_delete_like_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_delete_like_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_dislike_by_creator_when_page_is_private(self):
        pass

    def test_dislike_by_other_user_user_when_page_is_public(self):
        pass

    def test_dislike_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_dislike_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.post('/api/poll/22/comment/1/like/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_dislike_by_creator_when_page_is_private(self):
        pass

    def test_delete_dislike_by_other_user_user_when_page_is_public(self):
        pass

    def test_delete_dislike_by_other_user_when_page_is_private_and_other_user_is_follower(self):
        pass

    def test_delete_dislike_by_other_user_when_page_is_private_and_other_user_is_not_follower(self):
        user = User.objects.get(id=4)
        token = f'Bearer {str(AccessToken.for_user(user))}'
        response = self.client.delete('/api/poll/22/comment/1/dislike/', HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
