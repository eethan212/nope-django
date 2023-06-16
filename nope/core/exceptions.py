from rest_framework import exceptions
from django.core.exceptions import ValidationError


class APIValidationError(ValidationError):

    def __init__(self, message, code=None, params=None, **kwargs):
        super(APIValidationError, self).__init__(message, code=code, params=params)
        self.extra = kwargs


class RegisterError(Exception):
    pass


class RegisterOverError(Exception):
    pass


class RegisterStepError(Exception):
    pass


class LoginAuthenticationFailed(exceptions.AuthenticationFailed):
    pass


class TemplateMesgSendFailError(Exception):
    pass


class DataAPIRequestException(Exception):
    pass


class PhoneBindError(Exception):
    pass


class ApplyTypeError(Exception):
    pass


class UserAlreadySignupError(Exception):
    pass


class UserNameAlreadyExistsError(Exception):
    pass


class UserCateError(Exception):
    pass


class EventSignUpError(exceptions.NotFound):
    pass


class AuditRecordNotFoundError(exceptions.NotFound):
    pass
