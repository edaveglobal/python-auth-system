import random
import logging
from django.core.mail import send_mail
from auth_system.settings import EMAIL_HOST_USER
        
            
def send_account_otp(email , user, subject):
    otp = random.randint(1000, 9999)
    message = f'Hi {user.username},\n\nYour account one-time-password is {otp}. Kindly supply it to move forward in the process.\n\n\nCheers\nGathpay Team'
    email_from = EMAIL_HOST_USER
    recipient_list = [email,]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        logging.warning(e)
        return
    return otp

# def update_user_otp_model(type, instance, otp):
#     """ Instantiating User OTP Model to store otp. """
#     user_otp_obj = None
#     if type == "model":
#         user_otp_obj = UserOTP()
#         user_otp_obj.user = instance
#     elif type == "views":
#         user_otp_obj = UserOTP.objects.get(user=instance.id)
        
#     user_otp_obj.user_otp = otp
#     user_otp_obj.save()