from django.conf import settings
from django_oss_storage.backends import OssMediaStorage


def to_oss_url(path):
    return OssMediaStorage().url(path).replace(settings.MEDIA_URL, '/')
