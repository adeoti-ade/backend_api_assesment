from django.core.cache import cache

from rest_framework import serializers

from .utils import get_number_for_user

class SmsSerializer(serializers.Serializer):
    _to = serializers.CharField(
        max_length=20, 
        required=True,
        error_messages={
            'required': '_to is missing',
            'blank': '_to is invalid'
            }
        )
    _from = serializers.CharField(
        max_length=20, 
        required=True,
        error_messages={
            'required': '_from is missing', 
            'blank': '_to is invalid'
            }
        )
    _text = serializers.CharField(
        max_length=255, 
        required=True,
        error_messages={
            'required': '_text is missing',
            'blank': '_to is invalid'
            }
        )


class InBoundSMSSerializer(SmsSerializer):

    def validate__to(self, value):
        user = self.context.get("request").user
        get_number_for_user(
            user=user,
            number=value,
            method="_to"
        )

        return value


class OutBoundSMSSerializer(SmsSerializer):

    def validate(self, data):
        _from = data.get("_from")
        _to = data.get("_to")
        to_from_cache = cache.get(_from)
        print(_to)
        print(_from)
        print(to_from_cache)
        if to_from_cache == _to:
            raise serializers.ValidationError(
                f"sms from {_from} to {_to} blocked by STOP request"
            )

        return data

    def validate__from(self, value):
        user = self.context.get("request").user
        get_number_for_user(
            user=user,
            number=value,
            method="_from"
        )

        return value



class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    auth_id = serializers.CharField(max_length=50, required=True)
