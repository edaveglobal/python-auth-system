from rest_framework import status
from rest_framework.test import APITestCase
from configs import Configs


class UserRegisterWithEmailTest(APITestCase):
    config = Configs()
    
    def test_user_register_with_username(self):
        response = self.client.post(self.config.register_url, self.config.user_register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response), 2)


