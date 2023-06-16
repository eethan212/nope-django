import six
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from . import errcodes


class BaseError(object):
    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    serialize_attrs = ['code', 'message', 'http_status']

    def __init__(self, exc):
        self.exc = exc

    def serialize(self):
        content = {
            key: getattr(self.__class__, key)
            for key in dir(self.__class__)
            if key in self.__class__.serialize_attrs
        }
        if hasattr(self.exc, 'detail'):
            content['detail'] = self.exc.detail
        elif hasattr(self.exc, 'message'):
            content['detail'] = str(self.exc.message)
        else:
            content['detail'] = str(self.exc)
        return content


class SystemError(BaseError):
    code = errcodes.SYSTEM_ERROR
    # message = "服务器异常"
    message = _("Server exception.")


class NotAuthenticatedError(BaseError):
    http_status = status.HTTP_401_UNAUTHORIZED
    code = errcodes.NotAuthenticated
    # message = "您没有登录"
    message = _("You are not signed in.")


class LoginAuthenticationFailedError(BaseError):
    http_status = status.HTTP_403_FORBIDDEN
    code = errcodes.LoginAuthenticationFailed
    # message = "账号或密码不正确"
    message = _("Account or password is incorrect.")


class AuthenticationFailedError(BaseError):
    http_status = status.HTTP_403_FORBIDDEN
    code = errcodes.AuthenticationFailed
    # message = "您的登录状态已过期或已失效"
    message = _("Your login status has expired.")

    def serialize(self):
        content = super(AuthenticationFailedError, self).serialize()

        detail = getattr(self.exc, "detal", None)
        if not detail:
            content['message'] = six.text_type(detail)

        if 'CSRF' in str(self.exc):
            content['message'] = '验证失败，请稍后再试'
        return content


class PermissionDeniedError(BaseError):
    http_status = status.HTTP_403_FORBIDDEN
    code = errcodes.PermissionDenied
    # message = "您没有权限"
    message = _("You don't have permission.")


class ObjectDoesNotExistError(BaseError):
    http_status = status.HTTP_404_NOT_FOUND
    code = errcodes.Notfound
    # message = "资源不存在"
    message = _("Not exist.")


class DoesNotExistError(BaseError):
    http_status = status.HTTP_404_NOT_FOUND
    code = errcodes.Notfound
    # message = "资源不存在"
    message = _("Not exist.")


class NotFoundError(BaseError):
    http_status = status.HTTP_404_NOT_FOUND
    code = errcodes.Notfound
    # message = "资源未找到"
    message = _('Not found.')


class Http404Error(NotFoundError):
    pass


# class PhoneError(BaseError):
#     http_status = status.HTTP_400_BAD_REQUEST
#     code = errcodes.VALIDATOR_ERROR
#     message = "手机号码已被绑定"
#     # message = _("Verification failed.")


class ValidationErrorError(BaseError):
    http_status = status.HTTP_400_BAD_REQUEST
    code = errcodes.VALIDATOR_ERROR
    message = "验证失败"
    # message = _("Verification failed.")

    def serialize(self):
        content = super(ValidationErrorError, self).serialize()

        if 'phone' in content['detail'].keys():
            content['message'] = '手机号已被绑定'
        return content


class InvalidTokenError(BaseError):
    http_status = status.HTTP_401_UNAUTHORIZED
    code = errcodes.AUTH_CANCLED_ERROR
    # message = "认证失败"
    message = _("Authentication failed.")


class APIValidationErrorError(ValidationErrorError):
    http_status = status.HTTP_400_BAD_REQUEST
    code = errcodes.VALIDATOR_ERROR
    # message = "验证失败"
    message = _("Verification failed.")

    def serialize(self):
        content = super(APIValidationErrorError, self).serialize()
        content['code'] = getattr(self.exc, 'code', errcodes.VALIDATOR_ERROR)
        # if 'request' in self.exc.extra:
        #     self.exc.extra.pop('request')
        # content.update(self.exc.extra)
        return content


class APIExceptionError(BaseError):
    http_status = status.HTTP_400_BAD_REQUEST
    code = errcodes.SYSTEM_ERROR
    # message = "服务器异常"
    message = _("Server exception.")


class DataAPIRequestExceptionError(BaseError):
    http_status = status.HTTP_400_BAD_REQUEST
    code = errcodes.RESOURCE_UNAVAILABLE_ERROR
    # message = "数据服务不可用"
    message = _("Data service is not available.")


class DataAPIResponseExceptionError(BaseError):
    code = errcodes.RESOURCE_ABNORMAL_ERROR
    # message = "数据请求返回出错"
    message = _("Data request returned error.")


class SignInActivityErrorError(BaseError):
    code = errcodes.RESOURCE_ABNORMAL_ERROR
    # message = "用户已经签到"
    message = _("The user has signed in.")
