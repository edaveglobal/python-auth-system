import logging
from auth_system.settings import EMAIL_HOST_USER
from smtplib import SMTPException
from django.core.mail import send_mail


def send_customer_message(email_from, subject, message, username):
    recipient_list = [EMAIL_HOST_USER]
    message = message + f"\n\nFrom {username}"
    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPException as e:
        logging.debug('There was an error sending the custommer message. ' + e)
        return

