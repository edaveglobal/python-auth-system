from rest_framework import serializers

from .models import CustomerWallet


class GathpayCustomerWalletSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerWallet
        fields = "__all__"



