from django.core.mail import send_mail
from auth_system.settings import EMAIL_HOST_USER
import random
        
            
def send_account_otp(email , user, subject):
    otp = random.randint(1000, 9,999)
    message = f'Hi {user.username}, Your one-time-password is {otp}.'
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(e)
    return True