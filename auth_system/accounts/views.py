
import logging
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.cache import cache

# from .models import UserVerifiedModel
from .thread import SendAccountOTP, SendForgotPasswordOTP
from .cache import get_cached_otp_for, set_otp_cache_for
from .models import update_user_verified_for

from .serializers import (
    GathpayUserAccountRegisterSerializer,
    GathpayUsersAccountSerializer,
    ResetPasswordAccountSerializer,
    UpdateUserAccountPasswordSerializer
)
from django.contrib.auth.models import User


#redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class APIResponse:
    
    @staticmethod
    def send(message, status, err=""):
        return Response(
            {
                "message": message,
                "statu_code": status,
                "error": err
            }
        ) 

class GathpayUsersAccount(APIView):
    """ Authorized Specific Users Account View"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GathpayUserAccountRegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message=f"Gathpay user {data['first_name']} account is successfully registered. Kindly check your mail for OTP.",
                status=status.HTTP_201_CREATED,
            )
        return APIResponse.send(
                message=f"User with first name {data['first_name']} failed to register.",
                status=status.HTTP_400_BAD_REQUEST,
            )


class GathpayUsersAccounts(APIView):
    """ Authorized Specific Users Accounts View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all().order_by('id')
        except Exception as err:
            logging.debug(err)
            return Response({
                "message": "Internal server error. Unable to fetch users' accounts.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": err
            })

        serializer = GathpayUsersAccountSerializer
        if serializer.is_valid:
            users = serializer(users, many=True).data
            return Response({
                "message": "Successfully fetched Gathpay users' accounts.",
                "status_code": status.HTTP_200_OK,
                "total_querysets": len(users),
                "accounts": users
            })
        return Response({
            "message": serializer.errors,
            "status_code": status.HTTP_409_CONFLICT,
        })


class GathpayUserAccount(APIView):
    """ Authorized Specific User Account View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """ Specific User Account Fetch """
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            logging.debug(err)
            return Response({
                "message": f"Gathpay user account with id {pk} not found.",
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })

        serializer = GathpayUsersAccountSerializer

        if serializer.is_valid:
            data = serializer(user, many=False).data
            return Response({
                "message": f"Gathpay user account {pk} found successfully.",
                "status_code": status.HTTP_200_OK,
                "user": data
            })
        return Response({
            "message": serializer.errors,
            "status_code": status.HTTP_409_CONFLICT
        })

    def put(self, request, pk, *args, **kwargs):
        """ User Account Details Update """
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            logging.warning(err)
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": str(err)}
            return Response(error)

        serializer = GathpayUsersAccountSerializer
        serializer = serializer(instance=user, data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            response = {
                "message": f"Gathpay user account with id {pk} is successfully updated.",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
                }

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully updated.",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors
            }
        return Response(error)

    def patch(self, request, pk, *args, **kwargs):
        """ User Account Details Patch"""
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            logging.warning(err)
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": str(err)}
            return Response(error)

        serializer = GathpayUsersAccountSerializer
        serializer = serializer(
            instance=user,
            data=request.data,
            context={'request': request},
            partial=True)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            response = {
                "message": f"Gathpay user account with id {pk} is not successfully patched.",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
                }

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully patched.",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors}
        return Response(error)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": f"Gathpay user account with id {pk} not found.",
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })

        user.delete()
        return Response({
            "message": f"Gathpay user account with id {pk} deleted successfully.",
            "status_code": status.HTTP_200_OK
        })



class GathpayUserChangePassword(APIView):
    """ This view is actually for an active/logged in user account."""
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UpdateUserAccountPasswordSerializer(
            data=request.data, instance=request.user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "Password updated successfully.",
                "status_code": status.HTTP_200_OK
            })
        return Response({
            "message": str(serializer.errors),
            "status_code": status.HTTP_409_CONFLICT
        })


class GathpayUserForgotPassword(APIView):
    """ Unathorized User Forgot Password View """

    permission_classes = []
    pass
    def post(self, request, *args, **kwargs): 

        try:
            user = User.objects.get(email=request.data['email'])
        except Exception as err:
            logging.debug(err)
            return Response({
                "message": f"Gathpay user account with email {request.data['email']} not found.",
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })
        # ''' EXCEUTING THREAD TO SEND OTP FOR FORGOT PASSWORD'''
        subject = "noreply@Gathpay: OTP required to reset your password."
        SendForgotPasswordOTP(subject=subject, email=user.email, user=user).start()
        return Response({
            "message": "Success. Check your email for otp.",
            "status_code": status.HTTP_200_OK
            })

class GathpayUserResetPassword(APIView):
    """ Unauthorized User Account Reset Password View"""
    permission_classes = []
    pass
    def post(self, request, *args, **kwargs):
        
        OTP = request.data['otp']
        try:
            cached_username = get_cached_otp_for(otp=OTP, type="reset")
            user = User.objects.get(username=cached_username)
        except Exception as e:
            logging.debug(e)
            return  APIResponse.send(
                message="Catch missed. OTP not found.",
                status=status.HTTP_404_NOT_FOUND,
                err=str(e)
            )
        serializer = ResetPasswordAccountSerializer
        serializer = serializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                "message": "Success. Your password has been updated. Log in with your new password.",
                "status_code": status.HTTP_202_ACCEPTED
            })
        logging.debug('Serializer is not valid. ' + serializer.errors)
        return Response({
            "message": "Failed operation.",
            "status_code": status.HTTP_404_NOT_FOUND,
            "error": str(serializer.errors)
        })



class GathpayUserAccountActivate(APIView):
    """ Unauthorized User Account Activate View"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        OTP = request.data['otp']
        
        try:
            cached_otp = get_cached_otp_for(otp=OTP, type="verify")
        except Exception as e:
            logging.debug(e)
            return  APIResponse.send(
                message="Catch missed. OTP not found.",
                status=status.HTTP_404_NOT_FOUND,
            )
            
        if cached_otp == OTP:
            instance = User.objects.get(email=request.data['email'])
            update_user_verified_for(instance)
            return  APIResponse.send(
                message=f"Account verified successfully.",
                status=status.HTTP_200_OK,
            )
        
        return APIResponse.send(
                message=f"Account verification failed. OTP {OTP} supplied is not matched or expired.",
                status=status.HTTP_409_CONFLICT,
            )
        
        
class GathpayUserResendAccountOTP(APIView):
    permission_classes = []
    
    def post(request, *args, **kwargs):
        email = request.data['email']
        
        try:
            instance = User.objects.get(email=email)
        except Exception as e:
            logging.debug(e)
            return  APIResponse.send(
                message=f"Gathpay user account with email {email} not found.",
                status=status.HTTP_404_NOT_FOUND,
                error=str(e)
            )
        
        try:
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            subject = "noreply@Gathpay: Here is your OTP for account activation."
            SendAccountOTP(subject=subject, email=instance.email, user=instance).start()
            
        except SMTPException as e:
            logging.debug(e)
            return  APIResponse.send(
                message=f"Email verification OTP could not send.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=str(e)
            )
        
        return  APIResponse.send(
                message=f"Account verification OTP sent.",
                status=status.HTTP_200_OK,
            )