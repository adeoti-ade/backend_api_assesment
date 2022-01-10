from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Account, PhoneNumber
from .serializers import AccountSerializer, PhoneNumberSerializer


class AccountViewSet(ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer