from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault

from .models import CustomerWallet, CustomerReferralDetail



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
        
    # def save(self, validated_data, *args):
    #     referrer = CurrentUserDefault()
    #     referree_username=self.validated_data["referree_username"]
        # referral_detail_instance = CustomerReferralDetail.objects.create(
        #     referrer=referrer,
        #     referree_username=validated_data["referree_username"],
            
        # )

        # referral_detail_instance.save()
        # return referral_detail_instance




