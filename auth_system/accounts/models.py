import hashlib
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .thread import SendAccountOTP

class UserVerified(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_user_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    


@receiver(post_save, sender=User)
def send_activation_email_otp(sender, instance, created, **kwargs):
   
    if created:
        try:
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            subject = "noreply@Gathpay: Here is your OTP for account activation."
            SendAccountOTP(subject=subject, email=instance.email, user=instance).start()

        except Exception as e:
            logging.debug(e)
            return
        # update_user_verified_for(instance)
        
def update_user_verified_for(instance):
        user_verified_obj = UserVerified()
        user_verified_obj.user = instance
        user_verified_obj.is_user_verified = True
        user_verified_obj.save()