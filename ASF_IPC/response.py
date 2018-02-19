# -*- coding: utf-8 -*-
from http.client import responses

from . import error


class GenericResponse(object):

    def __init__(self, response):
        code = response.status_code
        error = None
        try:
            json_content = response.json()
            self.message = json_content.get('Message')
            self.result = json_content.get('Result')
            self.success = json_content.get('Success')
            if not self.success:
                error = self.message
        except ValueError:
            self.message = ''
            self.result = response.text
            self.success = False
            error = responses[code]
        if not self.success:
            raise error.ASF_ResponseError(error, code)
