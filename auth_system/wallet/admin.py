from django.contrib import admin
from .models import CustomerWallet,  CustomerReferralDetail


# Register your models here.
class CustomerWalletAdmin(admin.ModelAdmin):
    list_display = ("customer", "updated_wallet_at")
    
    
admin.site.register(CustomerWallet, CustomerWalletAdmin)

class CustomerReferralDetailAdmin(admin.ModelAdmin):
    list_display = ("referrer", "referrals")
    

admin.site.register(CustomerReferralDetail, CustomerReferralDetailAdmin)
