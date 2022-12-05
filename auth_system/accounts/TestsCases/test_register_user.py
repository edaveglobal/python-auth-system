from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .configs import Configs
from django.contrib.auth.models import User

from accounts.serializers import *


class UserRegisterWithEmailTest(TestCase):
    config = Configs()

    client = Client()

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            **self.config.user_register_data
        )
    
    # def test_user_register_with_username(self):
    #     response = self.client.post(self.config.register_url, self.config.user_register_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len(response), 2)

    def test_user_create(self):
        response = self.client.get('http://localhost:8000/api/v1/users/account/<int: pk>/', kwargs={"pk": self.test_user.pk}, format="json")
        test_user = User.objects.get(pk=self.test_user.pk)
        serializer = GathpayUsersAccountSerializer(data=test_user, many=False).is_valid()
        print(response, serializer)
        #self.assertEqual(response.statusCode, )
        #self.assertContains(status_code=status.HTTP_201_CREATED)


