# -*- coding: utf-8 -*-


class ASF_Error(Exception):

    def __init__(self, message):
        super(ASF_Error, self).__init__()
        self.message = message

    def __str__(self):
        return self.message


class ASF_BadRequest(ASF_Error):

    def __init__(self, message):
        super(ASF_BadRequest, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_Unauthorized(ASF_Error):

    def __init__(self, message):
        super(ASF_Unauthorized, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_Forbidden(ASF_Error):

    def __init__(self, message):
        super(ASF_Forbidden, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_NotFound(ASF_Error):

    def __init__(self, message):
        super(ASF_NotFound, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_NotAllowed(ASF_Error):

    def __init__(self, message):
        super(ASF_NotAllowed, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_NotAcceptable(ASF_Error):

    def __init__(self, message):
        super(ASF_NotAcceptable, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_LengthRequired(ASF_Error):

    def __init__(self, message):
        super(ASF_LengthRequired, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_InternalServerError(ASF_Error):

    def __init__(self, message):
        super(ASF_InternalServerError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ASF_NotImplemented(ASF_Error):

    def __init__(self, message):
        super(ASF_NotImplemented, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message
