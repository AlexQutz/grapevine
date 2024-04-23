from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
import base64

User = get_user_model()

class CustomBasicAuthenticationBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Basic '):
            return None
        
        # Remove the 'Basic ' prefix from the authorization header
        credentials_b64 = authorization_header[len('Basic '):]
        
        try:
            # Decode the base64-encoded credentials
            credentials = base64.b64decode(credentials_b64).decode('utf-8')
            # Split the credentials into username and password
            username, password = credentials.split(':')
        except (ValueError, UnicodeDecodeError):
            return None
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        
        return None