

import threading
from auth_system.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .helpers import send_account_otp
import logging

class SendAccountActivationEmail(threading.Thread):
    
    def __init__(self , email , user):
        self.email = email
        self.user = user
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = "noreply: Activate your user's account."
            send_account_otp(self.email, self.user, subject)
        except Exception as e:
            print(e)
            logging.warning(e)
            


class SendForgetPasswordEmail(threading.Thread):
    
    def __init__(self , email , user):
        self.email = email
        self.user = user
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = 'noreply: Your forget password otp.'
            send_account_otp(self.email, self.user, subject)
        except Exception as e:
            print(e)
            logging.warn(e)