from django.conf import settings
from rest_framework import authentication
from django.contrib.auth.backends import UserModel


class LaravelAuth(authentication.BaseAuthentication):

    def authenticate_header(self, request):
        return 'ok'

    def authenticate(self, request, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION') == f'Bearer {settings.SECRET_KEY * 2}':
            try:
                user = UserModel.objects.get(pk=1)
            except UserModel.DoesNotExist:
                return
            return user, 'ok'
        return
