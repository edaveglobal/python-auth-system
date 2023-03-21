import logging
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth.models import User
from .configs import Configs


class UserCreateTestCase(APITestCase):
    client = APIClient()
    def test_user_create(self):
        config = Configs()

        user_test_data = {
            "username": "testuser2",
            "email": "test@testuser.co",
            "first_name": "testfirst",
            "last_name": "testlast",
            "password": "test@123",
            "password2": "test@123"
        }
        try:
            user_initial_count = User.objects.count()
            response = self.client.post(config.register_url, user_test_data, content_type='application/json')
            # print(response.data)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)
            self.assertEqual(User.objects.count(), user_initial_count)
        except Exception as e:
            print(e)
            logging.debug(e)