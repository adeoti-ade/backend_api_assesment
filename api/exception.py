from rest_framework import exceptions, status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response
    if response is not None:
        customized_response = {"message": "", 'errors': {}}

        for key, value in response.data.items():
            customized_response['errors'][key] = value

        response.data = customized_response

    return response