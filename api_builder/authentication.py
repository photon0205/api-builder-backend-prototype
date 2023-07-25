from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import API

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization', '')

        if not api_key.strip() or api_key.lower() == 'none':
            raise AuthenticationFailed('No API key provided.')

        api_key = api_key.split()[-1]

        try:
            api = API.objects.get(access_key=api_key)
        except API.DoesNotExist:
            raise AuthenticationFailed('API key is invalid.')

        return (api, None)
