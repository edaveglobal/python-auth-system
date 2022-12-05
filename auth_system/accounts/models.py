
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
from .thread import SendAccountActivationEmail , SendForgetPasswordEmail
from .thread import *



class UserOTP(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    user_otp = models.CharField(max_length=10 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            subject = "noreply: Here is your OTP for account activation."
            otp = send_account_otp(email=instance.email, user=instance, subject=subject)
            forget_password_user = UserOTP()
            forget_password_user.user = instance
            forget_password_user.user_otp = otp
            forget_password_user.save()
            logging.info(f"Email delivered to {instance.email} around {time.now()}")
            # ''' EXCEUTING THREAD TO SEND EMAIL '''
            #SendAccountActivationEmail(email=instance.email, user=instance).start()
    except Exception as e:
        logging.warning(e)