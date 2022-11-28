
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .helpers import send_account_otp
from .models import ForgetPassword

from .serializers import (
    GathpayUserAccountRegisterSerializer,
    GathpayUsersAccountSerializer,
    ForgetPasswordAccountSerializer,
    UpdateUserAccountPasswordSerializer
)
from django.contrib.auth.models import User

class GathpayUsersAccount(APIView):
    """ Authorized Specific Users Account View"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GathpayUserAccountRegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # decision later
            # send_account_otp(serializer.data['email'], request.user)
            return Response(
                {
                    "message": f"Gathpay user {data['first_name']} account is successfully registered. Kindly check your mail for otp.",
                    "statusCode": status.HTTP_201_CREATED})
        return Response(
            {
                "message": f"User with first name {data['first_name']} failed to register.",
                "statusCode": status.HTTP_400_BAD_REQUEST})


class GathpayUsersAccounts(APIView):
    """ Authorized Specific Users Accounts View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all().order_by('id')
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": "Internal server error. Unable to fetch users' accounts.",
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": err
            })

        serializer = GathpayUsersAccountSerializer
        if serializer.is_valid:
            users = serializer(users, many=True).data
            return Response({
                "message": "Successfully fetched Gathpay users' accounts.",
                "statusCode": status.HTTP_200_OK,
                "accounts": users
            })
        return Response({
            "message": serializer.errors,
            "statusCode": status.HTTP_409_CONFLICT,
        })


class GathpayUserAccount(APIView):
    """ Authorized Specific User Account View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """ Specific User Account Fetch """
        try:
            user = User.objects.filter(id=pk).first()
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": f"Gathpay user account with id {pk} not found.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })

        serializer = GathpayUsersAccountSerializer

        if serializer.is_valid:
            data = serializer(user, many=False).data
            return Response({
                "message": f"Gathpay user account {pk} found successfully.",
                "statusCode": status.HTTP_200_OK,
                "user": data
            })
        return Response({
            "message": serializer.errors,
            "statusCode": status.HTTP_409_CONFLICT
        })

    def put(self, request, pk, *args, **kwargs):
        """ User Account Details Update """
        try:
            user = User.objects.filter(id=pk).first()
        except Exception as err:
            logging.warning(err)
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)}
            return Response(error)

        serializer = GathpayUsersAccountSerializer
        serializer = serializer(instance=user, data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            response = {
                "message": f"Gathpay user account with id {pk} is successfully updated.",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
                }

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully updated.",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors
            }
        return Response(error)

    def patch(self, request, pk, *args, **kwargs):
        """ User Account Details Patch"""
        try:
            user = User.objects.filter(id=pk).first()
        except Exception as err:
            logging.warning(err)
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
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
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
                }

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully patched.",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors}
        return Response(error)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.filter(id=pk).first()
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": f"Gathpay user account with id {pk} not found.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })

        user.delete()
        return Response({
            "message": f"Gathpay user account with id {pk} deleted successfully.",
            "statusCode": status.HTTP_200_OK
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
                "statuCode": status.HTTP_200_OK
            })
        return Response({
            "message": str(serializer.errors),
            "statuCode": status.HTTP_409_CONFLICT
        })


class GathpayUserForgotPassword(APIView):
    """ Unathorized User Forgot Password View """

    def post(self, request, *args, **kwargs): 

        try:
            user = User.objects.get(email=request.data['email'])
            
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": f"Gathpay user account with email {request.data['email']} not found.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })
        try:
            subject = "noreply: Your otp required to change password."
            otp = send_account_otp(email=user.email, user=user, subject=subject)
            forget_password_user = ForgetPassword.objects.get(user=user.id)
            forget_password_user.forget_password_otp = otp
            forget_password_user.save()
            return Response({
            "message": "Success. Check your email for otp.",
            "statuCode": status.HTTP_200_OK
             })
        except Exception as e:
            return Response({
            "message": "Failed to send otp.",
            "statuCode": status.HTTP_503_SERVICE_UNAVAILABLE
        })
            

class GathpayUserResetPassword(APIView):

    def post(self, request, *args, **kwargs):
        
        try:
            forget_password_user = ForgetPassword.objects.get(forget_password_otp=request.data['otp'])
        except Exception as err:
            logging.warning(err)
            return Response({
                "message": f"Gathpay user account with the one-time-password not found.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)
            })
        
        serializer = ForgetPasswordAccountSerializer
        serializer = serializer(instance=forget_password_user.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            forget_password_user.forget_password_otp = 0
            forget_password_user.save()
            return Response({
                "message": "Success. Your password has been updated.",
                "statuCode": status.HTTP_202_ACCEPTED
            })
        logging.warning(serializer.errors)
        return Response({
            "message": "Failed operation.",
            "statusCode": status.HTTP_404_NOT_FOUND,
            "error": str(serializer.errors)
        })

        