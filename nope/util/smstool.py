import pytz
import random
import string
import logging
from functools import partial
from django.conf import settings
from datetime import datetime, timedelta
from aliyun.sms import SMSEngine as AliyunSMSEngine
from nope.accounts.models import SMSRecord

log = logging.getLogger(__name__)


class SendSMSError(Exception):
    pass


class AliyunVerifyCodeSMSEngine(AliyunSMSEngine):
    TEMPLATE_CODE = settings.SMS_VERIFY_TEMPLATE_CODE
    # "SMS_188070151"
    SIGN_NAME = settings.PROJECT_NAME


class AliyunAbroadVerifyCodeSMSEngine(AliyunSMSEngine):
    TEMPLATE_CODE = settings.SMS_VERIFY_TEMPLATE_CODE
    # "SMS_188070151"
    SIGN_NAME = settings.PROJECT_NAME


class AliyunAppointNotifySMSEngine(AliyunSMSEngine):
    TEMPLATE_CODE = settings.SMS_NOTIFY_TEMPLATE_CODE
    # "SMS_193521172"
    SIGN_NAME = settings.PROJECT_NAME


class AliyunAbroadAppointNotifySMSEngine(AliyunSMSEngine):
    TEMPLATE_CODE = settings.SMS_NOTIFY_TEMPLATE_CODE
    # "SMS_190281906"
    SIGN_NAME = settings.PROJECT_NAME


_load_engine = lambda engine: partial(
    engine,
    settings.ALIYUN_SMS_ACCESS_KEY_ID,
    settings.ALIYUN_SMS_ACCESS_KEY_SECRET)


class SendSMSTool(object):
    valid_delta = timedelta(minutes=5)
    engine = _load_engine(AliyunVerifyCodeSMSEngine)

    def __init__(self, phone_number, area_code="86"):
        self.phone_number = phone_number
        self.area_code = area_code

    def fetch_param(self):
        return []

    def rate_validate(self, start, end, times):
        return SMSRecord.objects.filter(
            klass=self.__class__.__name__,
            phone_number=self.phone_number,
            created_at__gte=start,
            created_at__lt=end
        ).count() < times

    def interval_validate(self, interval):
        now = datetime.now(pytz.UTC)
        try:
            latest_rcd = SMSRecord.objects.filter(
                phone_number=self.phone_number,
                klass=self.__class__.__name__
            ).latest('id')
        except SMSRecord.DoesNotExist:
            return True
        return latest_rcd.created_at + interval < now

    def send(self):
        try:
            print(self.area_code, self.phone_number, self.fetch_param())
            engine = self.__class__.engine(
                phone_number="+%s%s" % (self.area_code, self.phone_number),
                template_params=self.fetch_param())
            engine.send()
        except Exception as exp:
            log.info(exp)
            raise SendSMSError(str(exp))

        SMSRecord.objects.create(
            klass=self.__class__.__name__,
            code=getattr(self, "code", ""),
            area_code=self.area_code,
            phone_number=self.phone_number,
            expired=datetime.now(pytz.UTC) + self.valid_delta)

    def verify(self, code):
        sms_record = SMSRecord.objects.filter(
            verified=False,
            area_code=self.area_code,
            phone_number=self.phone_number,
            code=code,
            expired__gt=datetime.now(pytz.UTC)
        ).latest('id')
        sms_record.verified = True
        sms_record.save()


class RegisterSMSCodeTool(SendSMSTool):

    def __init__(self, *args, **kwargs):
        self.code = ''.join(random.sample(string.digits, 6))
        super(RegisterSMSCodeTool, self).__init__(*args, **kwargs)

    def fetch_param(self):
        return {"code": self.code}


class AbroadRegisterSMSCodeTool(RegisterSMSCodeTool):
    engine = _load_engine(AliyunAbroadVerifyCodeSMSEngine)


class ResetPhoneSMSCodeTool(RegisterSMSCodeTool):
    pass


class AppointmentVerifyCodeTool(RegisterSMSCodeTool):
    pass


class AbroadAppointmentVerifyCodeTool(AbroadRegisterSMSCodeTool):
    engine = _load_engine(AliyunAbroadVerifyCodeSMSEngine)


class AppointmentNotifyTool(SendSMSTool):
    engine = _load_engine(AliyunAppointNotifySMSEngine)

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super(AppointmentNotifyTool, self).__init__(*args, **kwargs)

    def fetch_param(self):
        return {"title": self.instance.title, "vid": self.instance.id}


class AbroadAppointmentNotifyTool(AppointmentNotifyTool):
    engine = _load_engine(AliyunAbroadAppointNotifySMSEngine)


class NotifyReadSMSEngine(AliyunSMSEngine):
    TEMPLATE_CODE = settings.SMS_NOTIFY_TEMPLATE_CODE
    SIGN_NAME = settings.PROJECT_NAME


class NotifyReadTool(SendSMSTool):
    engine = _load_engine(NotifyReadSMSEngine)

    def __init__(self, instance, path, *args, **kwargs):
        self.instance = instance
        self.path = path or 'wx'
        super(NotifyReadTool, self).__init__(*args, **kwargs)

    def fetch_param(self):
        return {"title": self.instance.title, "path": self.path}
