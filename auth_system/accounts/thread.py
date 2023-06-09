import logging
import threading
from datetime import datetime
from smtplib import SMTPException

from .cache import set_otp_cache_for
from .email import send_account_otp


class SendAccountOTP(threading.Thread):
    def __init__(self, subject, email, user):
        self._email = email
        self._subject = subject
        self._user = user
        self._otp = (0,)
        threading.Thread.__init__(self)

    def run(self):
        try:
            self._otp = send_account_otp(
                email=self._email, user=self._user, subject=self._subject
            )
            set_otp_cache_for(otp=self._otp, type="verify")
            logging.info(
                f"Email service for account verification delivered to {self._user.username} around {datetime.now()}"
            )
        except SMTPException as e:
            logging.debug("There was an error sending an email. " + e)


class SendForgotPasswordOTP(threading.Thread):
    def __init__(self, subject, email, user):
        self._email = email
        self._subject = subject
        self._user = user
        self._otp = 0
        threading.Thread.__init__(self)

    def run(self):
        try:
            self._otp = send_account_otp(
                email=self._email, user=self._user, subject=self._subject
            )
            set_otp_cache_for(otp=self._otp, username=self._user.username, type="reset")
            logging.info(
                f"Email service for forgot password delivered to {self._user.username} around {datetime.now()}"
            )
        except SMTPException as e:
            logging.debug(e)
