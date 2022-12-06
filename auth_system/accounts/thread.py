
import threading
from .helpers import send_account_otp
import logging

class SendAccountActivationEmail(threading.Thread):
    
    def __init__(self , email , user):
        self._email = email
        self._user = user
        self._otp = ""
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = "noreply: Here is your OTP for account activation."
            self._otp = send_account_otp(email=self._email, user=self._user, subject=subject)
        except Exception as e:
            logging.warning(e)

    def get_user_otp(self):
        return self._otp


class SendForgetPasswordEmail(threading.Thread):
    
    def __init__(self , email , user):
        self._email = email
        self._user = user
        self._otp = ""
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = 'noreply: Your forgot password OTP.'
            self._otp = send_account_otp(self._email, self._user, subject)
        except Exception as e:
            logging.warning(e)