import logging
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .thread import SendAccountActivationEmail, SendForgetPasswordEmail



class UserOTP(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    user_otp = models.CharField(max_length=10 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def send_activation_email_otp(sender, instance, created, **kwargs):
    try:
        if created:

            # ''' EXCEUTING THREAD TO SEND EMAIL '''
            thread = SendAccountActivationEmail(email=instance.email, user=instance)
            # start thread
            thread.start()
            # join a new thread to unfinished one
            thread.join()
            otp = thread.get_user_otp()
            update_user_otp_model(instance, otp)

            logging.info(f"Email delivered to {instance.username} around {datetime.now()}")

    except Exception as e:
        logging.debug(e)


def update_user_otp_model(instance, otp):
    user_otp_obj = UserOTP()
    user_otp_obj.user = instance
    user_otp_obj.user_otp = otp
    user_otp_obj.save()
