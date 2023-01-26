from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomerWallet(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)
    got_referred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_wallet_at = models.DateTimeField(auto_now=True)
   
    
    def __str__(self):
        return self.customer
    

class CustomerReferralDetail(models.Model):
    referrer = models.ForeignKey(CustomerWallet, on_delete=models.CASCADE)
    referrals = models.IntegerField(default=0)
    referral_bonus = models.IntegerField(default=0)
    
    
    
    # def save(self, *args, **kwargs):
    #     self.customer_name = self.customer_name.capitalize()
    #     self.message = self.message.capitalize()
    #     self.subject = self.subject.capitalize()
    #     return super(ContactMessage, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.referrer
    
    

# @receiver(post_save, sender=CustomerReferralDetail)
# def update_referral_detail(sender, instance, created, **kwargs):

#     if created:
#         try:
#             """EXCEUTING THREAD TO UPDATE REFFERRAL DETAILS """
#             SendCustomerContactUsMessage(
#                 subject=instance.subject,
#                 email_from=instance.customer_email,
#                 message=instance.message,
#                 username=instance.customer_name,
#             ).start()

#         except Exception as e:
#             logging.debug("Failed to execute send customer message thread. " + e)
#             return