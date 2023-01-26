from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import APIResponse

from .serializers import GathpayCustomerWalletSerializer

# Create your views here.


class GathpayCustomerWallet(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        pass
    