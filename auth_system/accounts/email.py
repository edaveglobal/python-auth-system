import random
import logging
from django.core.mail import send_mail
from auth_system.settings import EMAIL_HOST_USER
        
            
def send_account_otp(email , user, subject):
    otp = random.randint(1000, 9999)
    message = f'Hi {user.username},\n\nYour account one-time-password is {otp}.\
        \nThis one-time-password will expire in the next 10 minutes.\
        \nKindly supply it to move forward in the pipeline.\n\n\nCheers\nGathpay Team'
    email_from = EMAIL_HOST_USER
    recipient_list = [email,]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        logging.warning(e)
        return
    return otp