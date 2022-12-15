import hashlib
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .thread import SendAccountOTP

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
            SendAccountOTP(subject=subject, email=instance.email, user=instance).start()

    except Exception as e:
        logging.debug(e)