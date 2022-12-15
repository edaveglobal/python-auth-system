import hashlib
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from celery.result import AsyncResult

from .thread import SendAccountOTP

class UserVerifiedModel(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_user_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    


@receiver(post_save, sender=User)
def send_activation_email_otp(sender, instance, created, **kwargs):
    try:
        if created:

            # ''' EXCEUTING THREAD TO SEND EMAIL '''
            subject = "noreply: Here is your OTP for account activation."
            SendAccountOTP(subject=subject, email=instance.email, user=instance).start()

    except Exception as e:
        logging.debug(e)
    
    update_user_verified_model(instance)
        
def update_user_verified_model(instance):
        user_verified_obj = UserVerifiedModel()
        user_verified_obj.user = instance
        user_verified_obj.is_user_verified = True
        user_verified_obj.save()