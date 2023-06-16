import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from nope.util.smstool import RegisterSMSCodeTool
from nope.util.oss import to_oss_url
from .models import User


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(help_text='验证码', write_only=True, required=False)

    def validate_code(self, value):
        r = re.compile("\d{4}")
        if not r.match(value):
            return False
        user = self.context.get('request').user
        params = self.context.get('params')
        area_code = params.get("area_code", "86")
        phone = params.get("phone", user.phone)
        try:
            RegisterSMSCodeTool(phone, area_code).verify(value)
        except Exception:
            raise serializers.ValidationError('verification code incorrect')
        return True

    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'fullname', 'avatar', 'code', 'sub_park', 'enterprise']

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        if data.get('avatar') and not data['avatar'].startswith('http'):
            data['avatar'] = to_oss_url(data['avatar'])
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(max_length=255, read_only=True, source='token.access')
    refresh_token = serializers.CharField(max_length=255, read_only=True, source='token.refresh')

    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'access_token', 'refresh_token']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    # phone = serializers.CharField(max_length=11)
    # code = serializers.CharField(max_length=8, write_only=True)

    class Meta:
        fields = ['username', 'phone', 'password', 'code']

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if user.is_deleted:
            raise serializers.ValidationError('User is disabled.')

        return user


class SMSCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(help_text='电话')
    area_code = serializers.CharField(help_text='区号 默认为86', default='86')

    class Meta:
        fields = ['phone', 'area_code', 'code']
