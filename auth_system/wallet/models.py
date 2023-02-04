import logging 
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerWallet(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_wallet_at = models.DateTimeField(auto_now=True)
   
    
    def __str__(self):
        return self.customer.username
    

class CustomerReferralDetail(models.Model):
    referrer =  models.CharField(max_length=250)
    referree = models.CharField(max_length=250)
    referrals = models.IntegerField(default=0)
    referral_bonus = models.IntegerField(default=0)
    referred_at = models.DateTimeField(auto_now=True)
    
    
    
    def save(self, *args, **kwargs):
        self.referrals += 1
        self.referral_bonus += 5
        return super(CustomerReferralDetail, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.referrer.username
    
    

@receiver(post_save, sender=User)
def create_default_customer_wallet(sender, instance, created, **kwargs):

    if created:
        try:
            """EXCEUTING THREAD TO CREATE CUSTOMER WALLET """
            update_customer_wallet_for(instance)
            logging.info(f"Default customer wallet created for {instance.username} at {datetime.now()}")
        except SystemError as e:
            logging.debug("Failed create default customer wallet. " + e)
            return
        
def update_customer_wallet_for(instance):
    wallet = CustomerWallet()
    wallet.customer = instance
    wallet.save()