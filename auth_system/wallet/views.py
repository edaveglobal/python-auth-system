from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GathpayCustomerWalletSerializer, GathpayCustomerReferralDetailSerializer
from .models import CustomerWallet
# Create your views here.


class APIResponse:
    @staticmethod
    def send(message, status, data=dict(), err=""):
        return Response({"message": message, "status_code": status, "data": data, "error": err})



class GathpayCustomerWallet(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            wallet = CustomerWallet.objects.get(customer=request.user)
        except Exception as err:
            return APIResponse.send(
                message=f"Failed to fetch {request.user} wallet.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(err)
            )
        serializer = GathpayCustomerWalletSerializer
        if serializer.is_valid:
            customer_wallet = serializer(wallet, many=False).data
            return APIResponse.send(
                message=f"Success. Customer {request.user} wallet details fetched.",
                status=status.HTTP_200_OK,
                data=customer_wallet
            )
        return APIResponse.send(
                message="Oops. Some server serializing request errors.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
            )
        
    
    def patch(self, request, *args, **kwargs):
        try:
            wallet = CustomerWallet.objects.get(customer=request.user)
        except Exception as err:
            return APIResponse.send(
                message=f"Failed to fetch {request.user} wallet.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(err)
            )
        serializer = GathpayCustomerWalletSerializer(instance=wallet, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message=f"Success. Customer {request.user} wallet details updated.",
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return APIResponse.send(
                message="Oops. Some server serializing request errors.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
        )
    
    
class GathpayCustomerRefrralDetail(APIView):
    
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        serializer = GathpayCustomerReferralDetailSerializer(data=request.data)
    
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message="Success. Your referral details have been saved.",
                status=status.HTTP_201_CREATED
            )
        logging.debug(serializer.error)
        return APIResponse.send(
                message="Failed. Encountered some errors.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
            )