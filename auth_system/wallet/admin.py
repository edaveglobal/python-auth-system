from django.contrib import admin
from .models import CustomerWallet,  CustomerReferralDetail, CustomerReferreeDetail


# Register your models here.
class CustomerWalletAdmin(admin.ModelAdmin):
    list_display = ("customer", "updated_wallet_at")
    
    
admin.site.register(CustomerWallet, CustomerWalletAdmin)

class CustomerReferralDetailAdmin(admin.ModelAdmin):
    list_display = ("referrer", "referrals", "latest_referree", "referred_at")
    

admin.site.register(CustomerReferralDetail, CustomerReferralDetailAdmin)


class CustomerReferreeDetailAdmin(admin.ModelAdmin):
    list_display = ("referrer", "referree", "referred_at")
    

admin.site.register(CustomerReferreeDetail, CustomerReferreeDetailAdmin)
