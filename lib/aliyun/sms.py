from __future__ import absolute_import
import json
import uuid
import logging
from aliyunsms.services import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

log = logging.getLogger(__name__)


class RequestSMSError(Exception):

    def __init__(self, errcode="", message=None):
        self.errcode = errcode
        self.message = message

    def __str__(self):
        return "error code: %s\nerror message: %s" % (
            self.errcode, self.message)


class SMSEngine(object):
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"
    TEMPLATE_CODE = ""
    SIGN_NAME = ""

    sign_name = u"Ever永恒链动".encode('utf-8')

    def __init__(self, appkey, appsecret, *args, **kwargs):
        self.appkey = appkey
        self.appsecret = appsecret
        self.client = AcsClient(self.appkey, self.appsecret, self.REGION)
        self.args = args
        self.kwargs = kwargs
        region_provider.add_endpoint(
            self.PRODUCT_NAME,
            self.REGION, self.DOMAIN)

    def build_parmas(self):
        params = dict()
        params['from'] = self.ENGINE_CHANNEL
        params['to'] = self.kwargs['to']
        params['templateId'] = self.ENGINE_TEMPLATE_ID
        params['templateParas'] = self.kwargs.get('template_params', '')
        params['signature'] = self.ENGINE_SIGNATURE
        params['statusCallback'] = self.kwargs.get('callback')
        log.info("PARAMS: %s", str(params))
        return params

    def send(self):
        _request = SendSmsRequest.SendSmsRequest()
        _request.set_TemplateCode(self.TEMPLATE_CODE)
        _request.set_TemplateParam(self.kwargs.get("template_params", {}))
        _request.set_OutId(uuid.uuid1())
        _request.set_SignName(self.SIGN_NAME)
        _request.set_PhoneNumbers(self.kwargs.get("phone_number"))

        try:
            response = self.client.do_action_with_exception(_request)
            content = json.loads(response)
            if content['Code'] != 'OK':
                raise RequestSMSError(content["Code"], response.decode())
        except Exception as exp:
            raise RequestSMSError(str(exp))
