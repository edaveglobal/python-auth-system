
import threading
from .helpers import send_account_otp
import logging

class SendAccountOTP(threading.Thread):
    
    def __init__(self , subject, email , user):
        self._email = email
        self._subject = subject
        self._user = user
        self._otp = ""
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            self._otp = send_account_otp(email=self._email, user=self._user, subject=self._subject)
        except Exception as e:
            logging.warning(e)

    def get_user_otp(self):
        return self._otp