from datetime import datetime as dt
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import Http404
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import (
    UserSerializer,
    UserTokenSerializer,
    LoginSerializer,
    SMSCodeSerializer
)
from nope.util.smstool import (
    RegisterSMSCodeTool,
    AbroadRegisterSMSCodeTool,
)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    filterset_fields = []
    ordering_fields = ['created_at', 'id']
    ordering = ['id']

    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer})
    @action(detail=True, methods=['put'])
    def set_password(self, request, *args, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION') == f'Bearer {settings.SECRET_KEY * 2}':
            raise Http404
        user = self.get_object()
        password = request.data.get('password') or user.username[-8:]
        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True,
            context={'request': request, 'params': request.data}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if not request.user.first_login_time:
            request.user.first_login_time = dt.now()
            request.user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response(UserTokenSerializer(user).data)


class LogoutAPIView(generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendSMSCodeAPIView(generics.GenericAPIView):
    serializer_class = SMSCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SMSCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        area_code = serializer.validated_data.get('area_code')
        if area_code == '86':
            RegisterSMSCodeTool(phone, area_code).send()
        else:
            AbroadRegisterSMSCodeTool(phone, area_code).send()
        return Response({}, status=status.HTTP_201_CREATED)
