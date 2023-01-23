from rest_framework import serializers

from .models import ContactMessage


class GathpayCustomerContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
