import logging
import secrets
from smtplib import SMTPException

from django.core.mail import send_mail

from auth_system.settings import EMAIL_HOST_USER


def send_account_otp(email, user, subject):
    otp = secrets.choice(range(1000, 10000))
    message = f"Hi {user.username},\n\nYour account one-time-password is {otp}.\
        \nThis one-time-password will expire in the next 10 minutes.\
        \nKindly supply it to move forward in the pipeline.\n\n\nCheers\nGathpay Team"
    email_from = EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPException as e:
        logging.debug("There was an error sending an email. " + e)
        return
    return otp
