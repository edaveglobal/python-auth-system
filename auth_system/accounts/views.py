
from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    GathpayUserAccountRegisterSerializer,
    GathpayUsersAccountSerializer,
    # UpdateUserPasswordSerializer
)
from django.contrib.auth.models import User

from accounts import serializers


class GathpayUsersAccount(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GathpayUserAccountRegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                {
                    "message": f"Gathpay user {data['first_name']} account is successfully registered.",
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


# class BlocboxUserView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):

#         try:
#             user = User.objects.get(id=pk)
#         except Exception as err:
#             print(err)
#             return Response({
#                 "message": f"Blocbox user account with id {pk} not found.",
#                 "statusCode": status.HTTP_404_NOT_FOUND,
#                 "error": str(err)
#             })

#         serializer = UserSerializer

#         if serializer.is_valid:
#             data = serializer(user, many=False).data
#             return Response({
#                 "message": f"Blocbox user account {pk} found successfully.",
#                 "statusCode": status.HTTP_200_OK,
#                 "user": data
#             })
#         return Response({
#             "message": serializer.errors,
#             "statusCode": status.HTTP_409_CONFLICT
#         })

#     def delete(self, request, pk, *args, **kwargs):
#         try:
#             user = User.objects.get(id=pk)
#         except Exception as err:
#             return Response({
#                 "message": f"Blocbox user account with id {pk} not found.",
#                 "statusCode": status.HTTP_404_NOT_FOUND,
#                 "error": str(err)
#             })

#         user.delete()
#         return Response({
#             "message": f"Blocbox user account {pk} deleted successfully.",
#             "statusCode": status.HTTP_200_OK
#         })


# class ChangeBlocboxUserPasswordView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, *args, **kwargs):
#         serializer = UpdateUserPasswordSerializer(
#             data=request.data, instance=request.user)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({
#                 "message": "Password updated successfully.",
#                 "statuCode": status.HTTP_200_OK
#             })
#         return Response({
#             "message": str(serializer.errors),
#             "statuCode": status.HTTP_409_CONFLICT
#         })