from django.contrib import admin
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'received_at')
    
admin.site.register(ContactMessage, ContactMessageAdmin)
# Register your models here.
