from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken

from nope.core.models import TimestampMixin, DeleteMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, last_login=timezone.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(TimestampMixin, DeleteMixin, AbstractBaseUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'admin'
        NORMAL = 'normal', 'normal'

    username = models.CharField(help_text='username', max_length=255, unique=True)
    password = models.CharField(help_text='password', max_length=128)
    phone = models.CharField(help_text='phone', max_length=255, unique=True, null=True, blank=True)
    avatar = models.URLField(help_text='avatar', max_length=1024, null=True, blank=True)
    fullname = models.CharField(help_text='fullname', max_length=255, null=True, blank=True)
    first_login_time = models.DateTimeField(default=None, null=True, blank=True)
    role = models.CharField(help_text='role', max_length=16, null=True, blank=True,
                            choices=Role.choices, default=Role.NORMAL)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'nope_users'
        verbose_name = 'users'
        verbose_name_plural = 'users'

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class SMSRecord(TimestampMixin):
    area_code = models.CharField(help_text='区号', max_length=8, default="86")
    phone_number = models.CharField(help_text='电话', max_length=20, db_index=True)
    code = models.CharField(help_text='验证码', max_length=20)
    klass = models.CharField(help_text='验证模块', max_length=64, db_index=True)
    verified = models.BooleanField(help_text='验证标志', default=False, db_index=True)
    expired = models.DateTimeField()

    class Meta:
        db_table = 'nope_sms_record'
        verbose_name = "短信发送记录"
        verbose_name_plural = "短信发送记录"
