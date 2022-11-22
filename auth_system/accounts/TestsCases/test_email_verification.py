# from django.core import mail
# from rest_framework import status
# from rest_framework.test import APITestCase

# class EmailVerificationTest(APITestCase):

#     # endpoints needed
#     register_url = "/api/v1/users/accounts"
#     activate_url = "/api/v1/users/account/activation/"
#     login_url = "/api/v1/api/token/"
#     user_details_url = "/api/v1/users/accounts"
#     # user infofmation
#     user_data = {
#         "email": "test@example.com", 
#         "username": "test_user", 
#         "password": "verysecret"
#     }
#     login_data = {
#         "email": "test@example.com", 
#         "password": "verysecret"
#     }

#     def test_register_with_email_verification(self):
#         # register the new user
#         response = self.client.post(self.register_url, self.user_data, format="json")
#         # expected response 
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # expected one email to be send
#         self.assertEqual(len(mail.outbox), 1)
        
#         # parse email to get uid and token
#         email_lines = mail.outbox[0].body.splitlines()
#         # you can print email to check it
#         print(mail.outbox[0].subject)
#         print(mail.outbox[0].body)
#         activation_link = [l for l in email_lines if "/activate/" in l][0]
#         uid, token = activation_link.split("/")[-2:]
        
#         # verify email
#         data = {"uid": uid, "token": token}
#         response = self.client.post(self.activate_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         # login to get the authentication token
#         response = self.client.post(self.login_url, self.login_data, format="json")
#         self.assertTrue("auth_token" in response.json())
#         token = response.json()["auth_token"]

#         # set token in the header
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
#         # get user details
#         response = self.client.get(self.user_details_url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 1)
#         self.assertEqual(response.json()[0]["email"], self.user_data["email"])
#         self.assertEqual(response.json()[0]["username"], self.user_data["username"])


    
#     def test_register_resend_verification(self):
#         # register the new user
#         response = self.client.post(self.register_url, self.user_data, format="json")
#         # expected response 
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # expected one email to be send
#         # self.assertEqual(len(mail.outbox), 1)

#         # login to get the authentication token
#         response = self.client.post(self.login_url, self.login_data, format="json")
#         self.assertTrue("access" in response.json())
#         token = response.json()["access"]

#         # set token in the header
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
#         # try to get user details
#         response = self.client.get(self.user_details_url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#         # clear the auth_token in header
#         self.client.credentials()
#         # resend the verification email
#         data = {"email": self.user_data["email"]}
#         response = self.client.post(self.resend_verification_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
#         # there should be two emails in the outbox
#         self.assertEqual(len(mail.outbox), 2)

#         # parse the last email
#         email_lines = mail.outbox[1].body.splitlines()
#         activation_link = [l for l in email_lines if "/activate/" in l][0]
#         uid, token = activation_link.split("/")[-2:]
        
#         # verify the email
#         data = {"uid": uid, "token": token}
#         response = self.client.post(self.activate_url, data, format="json")
#         # email verified
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    

#     def test_resend_verification_wrong_email(self):
#         # register the new user
#         response = self.client.post(self.register_url, self.user_data, format="json")
#         # expected response 
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#         # resend the verification email but with WRONG email
#         data = {"email": self.user_data["email"]+"_this_email_is_wrong"}
#         response = self.client.post(self.resend_verification_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

#     def test_activate_with_wrong_uid_token(self):
#         # register the new user
#         response = self.client.post(self.register_url, self.user_data, format="json")
#         # expected response 
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#         # verify the email with wrong data
#         data = {"uid": "wrong-uid", "token": "wrong-token"}
#         response = self.client.post(self.activate_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)