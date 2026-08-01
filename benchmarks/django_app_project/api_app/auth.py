import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

class SimpleJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid token')

        class MockUser:
            is_authenticated = True
        return (MockUser(), None)
