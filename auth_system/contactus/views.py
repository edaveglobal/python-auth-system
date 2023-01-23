from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import APIResponse

from .serializers import GathpayCustomerContactUsSerializer


class GathpayCustomerContactUs(APIView):

    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = GathpayCustomerContactUsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return APIResponse.send(
                message="Success. Your contact us message is received.",
                status=status.HTTP_202_ACCEPTED,
            )

        return APIResponse.send(
            message="Failed. Some errors occured.",
            status=status.HTTP_400_BAD_REQUEST,
            err=string(serializer.error),
        )
