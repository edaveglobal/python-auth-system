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
    latest_referree = models.CharField(max_length=250, default="to_be_updated")
    referrals = models.IntegerField(default=0)
    referral_bonus = models.IntegerField(default=0)
    referred_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.referrer
    
    
class CustomerReferreeDetail(models.Model):
    referrer =  models.ForeignKey(CustomerReferralDetail, on_delete=models.CASCADE)
    referree = models.CharField(max_length=250)
    referred_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.referrer.referrer + " referred " + self.referree

@receiver(post_save, sender=User)
def create_default_customer_wallet_and_referral_details(sender, instance, created, **kwargs):

    if created:
        try:
            """EXCEUTING THREAD TO CREATE CUSTOMER WALLET """
            update_customer_wallet_for(instance)
            update_customer_referral_details_for(instance)
            logging.info(f"Default customer wallet and referral details created for {instance.username} at {datetime.now()}")
            
        except SystemError as e:
            logging.debug("Failed to create default customer wallet and referral details. " + e)
            return
        
        
@receiver(post_save, sender=CustomerReferralDetail)
def create_default_customer_referree_details(sender, instance, created, **kwargs):

    if created:
        try:
            """EXECUTING THREAD TO CREATE CUSTOMER WALLET"""
            instance.latest_referree = "init_referree"
            update_customer_referree_details_for(instance)
            logging.info(f"Customer referree details updated for {instance.referrer} at {datetime.now()}")
            
        except SystemError as e:
            logging.debug("Failed to create default customer wallet and referral details. " + e)
            return
    else:
        # this will be called for PATCH and PUT requests - because they both do not call model save method
        patched_customer_referree = instance
        update_customer_referree_details_for(patched_customer_referree)
        logging.info(f"Customer referree details patched for {instance.referrer} at {datetime.now()}")
        
def update_customer_wallet_for(instance):
    wallet = CustomerWallet()
    wallet.customer = instance
    wallet.save()
    
def update_customer_referral_details_for(instance):
    referral_detail = CustomerReferralDetail()
    referral_detail.referrer = instance.username
    referral_detail.save()
    
def update_customer_referree_details_for(instance):
    referree_detail = CustomerReferreeDetail()
    referree_detail.referrer = instance
    referree_detail.referree = instance.latest_referree
    referree_detail.save()