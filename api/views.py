from rest_framework import authentication, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Account, PhoneNumber
from .authentication import AccountAuthentication
from .serializers import SmsSerializer, TokenSerializer
from .utils import login_user


class InboundView(GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = SmsSerializer
    authentication_classes = [AccountAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()


class TokenView(GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        response = login_user(
            validated_data.get("username"),
            validated_data.get("auth_id")
        )

        return Response(response)