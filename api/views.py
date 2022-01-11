from django.core.cache import cache

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .authentication import AccountAuthentication
from .serializers import InBoundSMSSerializer, TokenSerializer, OutBoundSMSSerializer
from .utils import login_user


class InboundView(GenericAPIView):
    serializer_class = InBoundSMSSerializer
    authentication_classes = [AccountAuthentication]
    permission_classes = (IsAuthenticated,)
    cache_timeout = 60 * 60 * 4

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        _from = validated_data.get("_from")
        _to = validated_data.get("_to")
        cache.set(_to, _from, self.cache_timeout)
        data = {"message": "inbound sms ok", "error": ""}
        return Response(data)


class OutboundView(GenericAPIView):
    serializer_class = OutBoundSMSSerializer
    authentication_classes = [AccountAuthentication]
    permission_classes = (IsAuthenticated,)
    cache_timeout = 60 * 60 * 4

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = {"message": "outbound sms ok", "error": ""}
        return Response(data)


class TokenView(GenericAPIView):
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