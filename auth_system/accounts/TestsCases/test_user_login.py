from rest_framework.test import APITestCase
from rest_framework import status
from configs import Configs


class UserLoginTest(APITestCase):

    config = Configs()

    def test_user_login(self):
        response = self.client.post(self.config.login_url, self.config.user_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        # self.assertEqual(len(mail.outbox), 1)

        response = self.client.post(self.config.login_url, self.config.user_login_data, format="json")
        self.assertTrue("access" in response.json())
        token = response.json()["access"]

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.config.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response), 3)

        # clear the auth_token in header
        self.client.credentials()