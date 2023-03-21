class Configs:
   register_url = "http://localhost:8000/api/v1/users/account"
   login_url ='/api/token/'
   user_details_url ='/api/v1/users/accounts/'

   user_register_data = {
      'email':'test5@example.com',
      'username':'test_user5',
      'first_name':'test3',
      'last_name':'test3',
      'password':'verysecret'
   }
   user_login_data = {'username':'test_user','password':'verysecret'}
