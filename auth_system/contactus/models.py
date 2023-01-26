import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserVerified

from .thread import SendCustomerContactUsMessage


class ContactMessage(models.Model):

    customer_name = models.CharField(max_length=250)
    customer_email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.customer_name = self.customer_name.capitalize()
        self.message = self.message.capitalize()
        self.subject = self.subject.capitalize()
        return super(ContactMessage, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_name


@receiver(post_save, sender=ContactMessage)
def send_admin_message_for(sender, instance, created, **kwargs):

    if created:
        try:
            """EXCEUTING THREAD TO SEND CUSTOMER MESSAGE TO GATHPAY ADMIN"""
            SendCustomerContactUsMessage(
                subject=instance.subject,
                email_from=instance.customer_email,
                message=instance.message,
                username=instance.customer_name,
            ).start()

        except Exception as e:
            logging.debug("Failed to execute send customer message thread. " + e)
            return
