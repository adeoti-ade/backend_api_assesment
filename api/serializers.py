from django.core.cache import cache
from django.utils import timezone


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
            'blank': '_from is invalid'
            }
        )
    _text = serializers.CharField(
        max_length=255, 
        required=True,
        error_messages={
            'required': '_text is missing',
            'blank': '_text is invalid'
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
        if to_from_cache == _to:
            raise serializers.ValidationError(
                {
                    "_from": f"sms from {_from} to {_to} blocked by STOP request"
                }
            )

        cached_from_prefixed = "cached_"+_from
        cached_from = cache.get(cached_from_prefixed)
        if cached_from:
            api_count = cached_from.get("api_count")
            first_request_time = cached_from.get("first_request_time")
            diff = timezone.now() - first_request_time
            diff_in_hours = diff.total_seconds() / 3600

            if api_count == 50 and diff_in_hours < 24:
                raise serializers.ValidationError(
                    {
                        "_from": f"limit reached for from {_from}"
                    }
                )

            if int(diff_in_hours) == 24:
                cache.delete(cached_from_prefixed)

            cached_from["api_count"] = api_count+1
            cache.set(cached_from_prefixed, cached_from, 60 * 60 * 24)
        else:
            cache_data = {
                "api_count": 1,
                "first_request_time": timezone.now()
            }
            cache.set(cached_from_prefixed, cache_data, 60 * 60 * 24)

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
