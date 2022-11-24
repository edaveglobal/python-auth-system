# from django.db import models
import datetime, time
import uuid
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .thread import SendAccountActivationEmail , SendForgetPasswordEmail
from .tokens import account_activation_token

import uuid
from .thread import *


class ForgetPassword(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=250 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            token = account_activation_token.make_token(instance)
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            SendAccountActivationEmail(email=instance.email, user=instance).start()

    except Exception as e:
        print(e)
        
@receiver(post_save, sender=ForgetPassword)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            token = account_activation_token.make_token(instance)
            instance.forget_password_token = token
            SendForgetPasswordEmail(email=instance.email , user=instance.user).start()

    except Exception as e:
        print(e)