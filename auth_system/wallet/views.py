from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GathpayCustomerWalletSerializer, GathpayCustomerReferralDetailSerializer, GathpayCustomerReferreeDetailsSerializer
from .models import CustomerWallet, CustomerReferralDetail, CustomerReferreeDetail
# Create your views here.


class APIResponse:
    @staticmethod
    def send(message, status, data=dict(), err=""):
        return Response({"message": message, "status_code": status, "data": data, "error": err})



class GathpayCustomerWallet(APIView):
    """ GET and PATCH authorized requests on customer wallet """
    
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
                message=f"Failed to fetch {request.user} wallet details.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(err)
            )
        serializer = GathpayCustomerWalletSerializer(instance=wallet, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message=f"Success. Customer {request.user} wallet details updated.",
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        return APIResponse.send(
                message="Oops. Some server serializing request errors.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
        )
    
    
class GathpayCustomerReferral(APIView):
    """ PATCH unauthorized request on customer referral details """
    
    permission_classes = []
    
    def patch(self, request, *args, **kwargs):
        try:
            referral_detail_instance = CustomerReferralDetail.objects.get(referrer=request.data["referrer"])
        except CustomerReferralDetail.DoesNotExist as err:
            return APIResponse.send(
                message=f"Failed to fetch {request.data['referrer']} referral details.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(err)
            )
        
        serializer = GathpayCustomerReferralDetailSerializer(data=request.data, instance=referral_detail_instance, partial=True)
    
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message=f"Success. {request.data['referrer']} referral details have been updated.",
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        logging.debug(serializer.error)
        returnlatest_referree
    

class GathpayCustomerReferralDetails(APIView):
    """ GET authorized requests on customer referral details """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            referral_details_instance = CustomerReferralDetail.objects.filter(referrer=request.user.username)
        except CustomerReferralDetail.DoesNotExist as e:
            logging.debug(f"Failed to fetch referrer for this request user." + e)
            return APIResponse.send(
                message=f"Failed. No referral detail for the customer {request.user.username}.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(e)
            )
        
        serializer = GathpayCustomerReferralDetailSerializer
        
        if serializer.is_valid:
            data = serializer(referral_details_instance, many=True).data
            return APIResponse.send(
                message=f"Success. {request.user.username} referral details have been fetched.",
                status=status.HTTP_200_OK,
                data=data 
            )
            
        logging.debug(serializer.error)
        return APIResponse.send(
                message=f"Error. Serialized data is not valid.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
            )
class GathpayCustomerReferreeDetails(APIView):
    """ GET authorized requests on customer referree details """
     
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            referree_details_instance = CustomerReferreeDetail.objects.filter(referrer__referrer=request.user.username)
        except CustomerReferreeDetail.DoesNotExist as e:
            logging.debug(f"Failed to fetch referrer's referree details for this request user." + e)
            return APIResponse.send(
                message=f"Failed. No referree detail(s) for the customer {request.user.username}.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(e)
            )
        
        serializer = GathpayCustomerReferreeDetailsSerializer
        
        if serializer.is_valid:
            data = serializer(referree_details_instance, many=True).data
            return APIResponse.send(
                message=f"Success. {request.user.username} referree details have been fetched.",
                status=status.HTTP_200_OK,
                data=data 
            )
            
        logging.debug(serializer.error)
        return APIResponse.send(
                message=f"Error. Serialized data is not valid.",
                status=status.HTTP_400_BAD_REQUEST,
                err=str(serializer.error)
            )