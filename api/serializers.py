from django.db import models
from django.db.models import fields
from .models import Account, PhoneNumber
from rest_framework import serializers

class SmsSerializer(serializers.Serializer):
    _to = serializers.CharField(max_length=20, required=True)
    _from = serializers.CharField(max_length=20, required=True)
    _text = serializers.CharField(max_length=255, required=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    auth_id = serializers.CharField(max_length=50, required=True)
