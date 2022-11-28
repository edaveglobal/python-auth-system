from rest_framework import status
from django.test import TestCase
from .configs import Configs
from django.contrib.auth.models import User


class UserRegisterWithEmailTest(TestCase):
    config = Configs()

    def setUp(self) -> None:
        User.objects.create_user(
            **self.config.user_register_data
        )
    
    # def test_user_register_with_username(self):
    #     response = self.client.post(self.config.register_url, self.config.user_register_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len(response), 2)

    def test_user_create(self):
        test_user = User.objects.filter(email=self.config.user_register_data['email']).first()
        print(test_user.username)
        self.assertEqual(test_user.username, self.config.user_register_data['username'])
        #self.assertContains(status_code=status.HTTP_201_CREATED)


