import logging
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .thread import SendAccountOTP
# from .helpers import update_user_otp_model



class UserOTP(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    user_otp = models.CharField(max_length=20 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def send_activation_email_otp(sender, instance, created, **kwargs):
    try:
        if created:

            # ''' EXCEUTING THREAD TO SEND EMAIL '''
            subject = "noreply: Here is your OTP for account activation."
            thread = SendAccountOTP(subject=subject, email=instance.email, user=instance)
            # start thread
            thread.start()
            # this help to get the return otp from the thread
            thread.join()
            otp = thread.get_user_otp()
            update_user_otp_model(type="model", instance=instance, otp=otp)
            
            logging.info(f"Email delivered to {instance.username} around {datetime.now()}")

    except Exception as e:
        logging.debug(e)


def update_user_otp_model(type, instance, otp):
    """ Instantiating User OTP Model to store otp. """
    user_otp_obj = None
    if type == "model":
        user_otp_obj = UserOTP()
        user_otp_obj.user = instance
    elif type == "views":
        user_otp_obj = UserOTP.objects.get(user=instance.id)
        
    user_otp_obj.user_otp = otp
    user_otp_obj.save()