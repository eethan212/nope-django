# -*- coding: utf-8 -*-
import logging
import traceback
from django.core.exceptions import PermissionDenied
from rest_framework import response, views, exceptions
from django.http import Http404

from . import errors

log = logging.getLogger(__name__)


class ErrorHandler(object):

    def __init__(self, excp):
        self.excp = excp

    def parse(self):
        try:
            errmoudle = "%sError" % (self.excp.__class__.__name__)
            return getattr(errors, errmoudle)(self.excp).serialize()
        except AttributeError as err:
            log.info(err)
        return errors.SystemError(self.excp).serialize()

    def ErrorResponse(self, headers=None):
        err_content = self.parse()
        http_status = err_content.pop('http_status')
        return response.Response(err_content, http_status, headers=headers)


def handler(exc, context):

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    headers = dict()
    if isinstance(exc, exceptions.APIException):
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        views.set_rollback()

    log.info("APP API ERROR: \n%s", traceback.format_exc())
    return ErrorHandler(exc).ErrorResponse(headers=headers)


def simple_handler(exc, context):
    message = ''
    detail = ''

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if hasattr(exc, 'message'):
        message = exc.message
    else:
        message = exc.__class__.__name__

    if hasattr(exc, 'detail'):
        detail = exc.detail
    else:
        detail = str(exc)

    err_content = {
        'code': exc.status_code,
        'message': message,
        'detail': detail
    }

    return response.Response(err_content, exc.status_code)
