from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class UserRetrieveAPITest(APITestCase):
    fixtures = ['user_fixture']

    def test_retrieve_admin_by_unauthorized(self):
        unauthorized_response = self.client.get('/api/user/1/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_admin_by_other(self):
        other_user = get_user_model().objects.get(id=2)
        self.client.force_login(other_user)
        other_user_response = self.client.get('/api/user/1/')
        self.assertEqual(other_user_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_admin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.get('/api/user/1/')
        self.assertEqual(admin_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_user_response.data, {
            "id": 1,
            "username": "admin",
            "email": "admin@pollgram.local",
            "first_name": "Admin_first",
            "last_name": "Admin_last",
            "avatar": None,
            "cover": None,
            "bio": "Admin bio",
            "is_public": True,
            "is_verified": False,
            "followers_count": 0,
            "followings_count": 0
        })

    def test_retrieve_nonadmin_by_unauthorized(self):
        unauthorized_response = self.client.get('/api/user/2/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_nonadmin_by_other(self):
        other_user = get_user_model().objects.get(id=3)
        self.client.force_login(other_user)
        other_user_response = self.client.get('/api/user/2/')
        self.assertEqual(other_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(other_user_response.data, {
            "id": 2,
            "username": "sample",
            "email": "sample@pollgram.local",
            "first_name": "sample_first",
            "last_name": "sample_last",
            "avatar": None,
            "cover": None,
            "bio": "sample bio",
            "is_public": True,
            "is_verified": False,
            "followers_count": 0,
            "followings_count": 1
        })

    def test_retrieve_nonadmin_by_self(self):
        self_user = get_user_model().objects.get(id=2)
        self.client.force_login(self_user)
        self_user_response = self.client.get('/api/user/2/')
        self.assertEqual(self_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self_user_response.data, {
            "id": 2,
            "username": "sample",
            "email": "sample@pollgram.local",
            "first_name": "sample_first",
            "last_name": "sample_last",
            "avatar": None,
            "cover": None,
            "bio": "sample bio",
            "is_public": True,
            "is_verified": False,
            "followers_count": 0,
            "followings_count": 1
        })


    def test_retrieve_nonadmin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.get('/api/user/2/')
        self.assertEqual(admin_user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_user_response.data, {
            "id": 2,
            "username": "sample",
            "email": "sample@pollgram.local",
            "first_name": "sample_first",
            "last_name": "sample_last",
            "avatar": None,
            "cover": None,
            "bio": "sample bio",
            "is_public": True,
            "is_verified": False,
            "followers_count": 0,
            "followings_count": 1
        })

class UserUpdateAPITest(APITestCase):
    fixtures = ['user_fixture']
    
    def test_update_admin_by_unauthorized(self):
        unauthorized_response = self.client.put('/api/user/1/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_admin_by_other(self):
        other_user = get_user_model().objects.get(id=2)
        self.client.force_login(other_user)
        other_user_response = self.client.put('/api/user/1/')
        self.assertEqual(other_user_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_admin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.put('/api/user/1/',{
            'id': 2, # can't change
            "username": "admin1",
            "email": "admin1@pollgram.local",
            "first_name": "Admin1_first",
            "last_name": "Admin1_last",
            "avatar": "anything",
            "cover": "anything",
            "bio": "Admin1 bio",
            "is_public": False,
            "is_verified": True,
            "followers_count": 100, # can't change
            "followings_count": 100 # can't change
        }, format='json')
        self.assertEqual(admin_user_response.status_code, status.HTTP_200_OK)
        admin_user = get_user_model().objects.get(id=1)
        self.assertEqual(admin_user.username, "admin1")
        self.assertEqual(admin_user.email, "admin1@pollgram.local")
        self.assertEqual(admin_user.first_name, "Admin1_first")
        self.assertEqual(admin_user.last_name, "Admin1_last")
        self.assertFalse(bool(admin_user.avatar))
        self.assertFalse(bool(admin_user.cover))
        self.assertEqual(admin_user.bio, "Admin1 bio")
        self.assertFalse(admin_user.is_public)
        self.assertTrue(admin_user.is_verified)
        self.assertEqual(admin_user.get_followers().count(), 0)
        self.assertEqual(admin_user.get_followings().count(), 0)

    def test_update_nonadmin_by_unauthorized(self):
        unauthorized_response = self.client.put('/api/user/2/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_nonadmin_by_other(self):
        other_user = get_user_model().objects.get(id=3)
        self.client.force_login(other_user)
        other_user_response = self.client.put('/api/user/2/')
        self.assertEqual(other_user_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_nonadmin_by_self(self):
        self_user = get_user_model().objects.get(id=2)
        self.client.force_login(self_user)
        self_user_response = self.client.put('/api/user/2/',{
            "id": 1, # can't change
            "username": "sample1",
            "email": "sample1@pollgram.local", # can't change
            "first_name": "sample1_first",
            "last_name": "sample1_last",
            "avatar": "anything",
            "cover": "anything",
            "bio": "sample1 bio",
            "is_public": False,
            "is_verified": True, # can't change
            "followers_count": 100, # can't change
            "followings_count": 100 # can't change
        }, format='json')
        self.assertEqual(self_user_response.status_code, status.HTTP_200_OK)
        self_user = get_user_model().objects.get(id=2)
        self.assertEqual(self_user.username, "sample1")
        self.assertEqual(self_user.email, "sample@pollgram.local")
        self.assertEqual(self_user.first_name, "sample1_first")
        self.assertEqual(self_user.last_name, "sample1_last")
        self.assertFalse(bool(self_user.avatar))
        self.assertFalse(bool(self_user.cover))
        self.assertEqual(self_user.bio, "sample1 bio")
        self.assertFalse(self_user.is_public)
        self.assertFalse(self_user.is_verified)
        self.assertEqual(self_user.get_followers().count(), 0)
        self.assertEqual(self_user.get_followings().count(), 1)

    def test_update_nonadmin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.put('/api/user/2/',{
            "id": 1, # can't change
            "username": "sample1",
            "email": "sample1@pollgram.local",
            "first_name": "sample1_first",
            "last_name": "sample1_last",
            "avatar": "anything",
            "cover": "anything",
            "bio": "sample1 bio",
            "is_public": False,
            "is_verified": True,
            "followers_count": 100, # can't change
            "followings_count": 100 # can't change
        }, format='json')
        self.assertEqual(admin_user_response.status_code, status.HTTP_200_OK)
        sample_user = get_user_model().objects.get(id=2)
        self.assertEqual(sample_user.username, "sample1")
        self.assertEqual(sample_user.email, "sample1@pollgram.local")
        self.assertEqual(sample_user.first_name, "sample1_first")
        self.assertEqual(sample_user.last_name, "sample1_last")
        self.assertFalse(bool(sample_user.avatar))
        self.assertFalse(bool(sample_user.cover))
        self.assertEqual(sample_user.bio, "sample1 bio")
        self.assertFalse(sample_user.is_public)
        self.assertTrue(sample_user.is_verified)
        self.assertEqual(sample_user.get_followers().count(), 0)
        self.assertEqual(sample_user.get_followings().count(), 1)

class UserDestroyAPITest(APITestCase):
    fixtures = ['user_fixture']
    
    def test_destroy_admin_by_unauthorized(self):
        unauthorized_response = self.client.delete('/api/user/1/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_admin_by_other(self):
        other_user = get_user_model().objects.get(id=2)
        self.client.force_login(other_user)
        other_user_response = self.client.delete('/api/user/1/')
        self.assertEqual(other_user_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_admin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.delete('/api/user/1/')
        self.assertEqual(admin_user_response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_destroy_nonadmin_by_unauthorized(self):
        unauthorized_response = self.client.delete('/api/user/2/')
        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_nonadmin_by_other(self):
        other_user = get_user_model().objects.get(id=3)
        self.client.force_login(other_user)
        other_user_response = self.client.delete('/api/user/2/')
        self.assertEqual(other_user_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_nonadmin_by_self(self):
        self_user = get_user_model().objects.get(id=2)
        self.client.force_login(self_user)
        self_user_response = self.client.delete('/api/user/2/')
        self.assertEqual(self_user_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_nonadmin_by_admin(self):
        admin_user = get_user_model().objects.get(id=1)
        self.client.force_login(admin_user)
        admin_user_response = self.client.delete('/api/user/3/')
        self.assertEqual(admin_user_response.status_code, status.HTTP_204_NO_CONTENT)

# TODO: UserAvatarAPI and UserCoverApi test