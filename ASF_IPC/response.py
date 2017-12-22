# -*- coding: utf-8 -*-
from http.client import responses

from . import error


class GenericResponse(object):

    exceptions = {
        400: error.ASF_BadRequest,
        401: error.ASF_Unauthorized,
        403: error.ASF_Forbidden,
        404: error.ASF_NotFound,
        405: error.ASF_NotAllowed,
        406: error.ASF_NotAcceptable,
        411: error.ASF_LengthRequired,
        500: error.ASF_InternalServerError,
        501: error.ASF_NotImplemented
    }

    def __init__(self, response):
        self.code = response.status_code
        try:
            json_content = response.json()
            self.message = json_content.get('Message')
            self.result = json_content.get('Result')
            self.success = json_content.get('Success')
            if not self.success:
                self.error = self.message
        except ValueError:
            self.message = ''
            self.result = response.text
            self.success = False
            self.error = '{0} - {1}'.format(self.code, responses[self.code])
        if not self.success:
            if self.code in self.exceptions:
                raise self.exceptions[self.code](self.error)
            else:
                raise error.ASF_Error(self.error)
