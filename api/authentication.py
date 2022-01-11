from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Account


class AccountAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication.
        `authenticate` has two possible return values:
        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.
        2) `(user, token)` - We return a user/token combination when
                             authentication is successful.
                            If neither case is met, that means there's an error
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed`
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None
        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT
        # that we should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None
        # The JWT library we're using can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # we simply have to decode `prefix` and `token`. This does not make for
        # clean code, but it is a good decision because we would get an error
        # if we didn't decode these values.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        jwt = JWTAuthentication()
        validated_token = jwt.get_validated_token(str(token))
        validated_user = jwt.get_user(validated_token)

        try:
            user = Account.objects.get(pk=validated_user.pk)
        except Account.DoesNotExist:
            return None

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        return user, token