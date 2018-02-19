# -*- coding: utf-8 -*-
import json
from http.client import responses

from . import error


class GenericResponse(object):

    def __init__(self, response):
        code = response.status_code
        message = ''
        try:
            json_content = response.json()
            self.message = json_content.get('Message')
            self.result = json_content.get('Result')
            self.success = json_content.get('Success')
            if not self.success:
                message = self.message
        except ValueError:
            self.message = ''
            self.result = response.text
            self.success = False
            message = responses[code]
        if not self.success:
            raise error.ASF_ResponseError(message, code)

class WebsocketResponse(object):

    def __init__(self, response):
        message = ''
        try:
            json_content = json.loads(response)
            self.message = json_content.get('Message')
            self.result = json_content.get('Result')
            self.success = json_content.get('Success')
            if not self.success:
                message = self.message
        except ValueError:
            self.message = ''
            self.result = response.text
            self.success = False
            message = response.text
        if not self.success:
            raise error.ASF_ResponseError(message)
