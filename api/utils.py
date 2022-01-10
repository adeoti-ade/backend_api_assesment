from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account


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