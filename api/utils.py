from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, PhoneNumber


def login_user(username, auth_id):
    user = Account.objects.filter(username=username, password=auth_id).first()
    if user is None:
        raise serializers.ValidationError(
                {
                    "email": ["invalid login details"]
                }
            )

    refresh = RefreshToken.for_user(user)

    return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

def get_number_for_user(user: Account, number, method):
    receiver_qs = user.phonenumber_set.filter(number=number).first()
    if not receiver_qs:
        raise serializers.ValidationError(f"{method} parameter not found")

def create_account_with_phone_numbers(number="08133703766"):
    account, _ = Account.objects.get_or_create(
        username="awer",
        password="12345671"
    )
    PhoneNumber.objects.create(
        number=number,
        account=account
    )

    return account
