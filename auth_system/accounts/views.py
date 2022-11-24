from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .helpers import send_account_otp

from .serializers import (
    GathpayUserAccountRegisterSerializer,
    GathpayUsersAccountSerializer,
    GathpayUserAccountUpdateSerializer,
    UpdateUserAccountPasswordSerializer
)
from django.contrib.auth.models import User

class GathpayUsersAccount(APIView):
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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all().order_by('id')
        except Exception as err:
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

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):

        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            print(err)
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
        try:
            user = User.objects.get(pk=pk)
        except Exception as err:
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)}
            return Response(error)

        serializer = GathpayUserAccountUpdateSerializer
        serializer = serializer(instance=request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            response = {
                "message": f"Gathpay user account with id {pk} is successfully updated.",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data}

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully updated.",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors}
        return Response(error)

    def patch(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
            error = {
                "message": f"Gathpay user account with id {pk} does not exist.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "error": str(err)}
            return Response(error)

        incoming_data = request.data
        serializer = GathpayUserAccountUpdateSerializer
        serializer = serializer(
            instance=user,
            data=incoming_data,
            partial=True)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            response = {
                "message": f"Gathpay user account with id {pk} is not successfully patched.",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data}

            return Response(response)

        error = {
            "message": f"Gathpay user account with id {pk} is not successfully patched.",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "error": serializer.errors}
        return Response(error)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
        except Exception as err:
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


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GathpayUserAccountUpdateSerializer

class GathpayUserAccountChangePassword(APIView):
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
