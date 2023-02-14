import os

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault

from .models import CustomerWallet, CustomerReferralDetail, CustomerReferreeDetail



class GathpayCustomerWalletSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerWallet
        fields = ("customer", "balance", "updated_wallet_at")
    

    def get_customer(self, obj):
        return obj.customer.username
    
    def update(self, instance, validated_data):
        customer = self.context["request"].user

        if customer.pk != instance.customer.pk:
            raise serializers.ValidationError(
                {
                    "Authorize Errors": "You do not have permission to update the customer's balance."
                }
            )
        instance.balance = validated_data["balance"]
        instance.save()
        return instance
        

class GathpayCustomerReferralDetailSerializer(serializers.ModelSerializer):
    referrals = serializers.IntegerField(required=False)
    referral_bonus = serializers.IntegerField(required=False)
    
    class Meta:
        model = CustomerReferralDetail
        fields = "__all__"
        
    def update(self, instance, validated_data):
        instance.latest_referree = validated_data["latest_referree"]
        instance.referrals += int(os.getenv("REFERRAL_VALUE"))
        instance.referral_bonus +=  int(os.getenv("REFERRAL_BONUS")) #subject to change later
        instance.save()
        return instance



