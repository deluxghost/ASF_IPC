# -*- coding: utf-8 -*-


class ASF_Error(Exception):

    def __init__(self, message):
        super(ASF_Error, self).__init__()
        self.message = message

    def __repr__(self):
        classname = self.__class__.__name__
        return '{0}({1})'.format(classname, repr(self.message))

    def __str__(self):
        classname = self.__class__.__name__
        return '{0}: {1}'.format(classname, self.message)


class ASF_ResponseError(ASF_Error):

    def __init__(self, message, code=None):
        super(ASF_ResponseError, self).__init__(message)
        self.code = code

    def __repr__(self):
        classname = self.__class__.__name__
        if self.code:
            return '{0}({1}, {2})'.format(classname, repr(self.message), repr(self.code))
        return '{0}({1})'.format(classname, repr(self.message))

    def __str__(self):
        classname = self.__class__.__name__
        if self.code:
            return '{0}: {1} - {2}'.format(classname, self.code, self.message)
        return '{0}: {1}'.format(classname, self.message)


class ASF_ConnectionError(ASF_Error):

    def __init__(self, url):
        super(ASF_ConnectionError, self).__init__('')
        self.url = url
        self.message = 'Cannot establish connection to: {0}'.format(url)

    def __repr__(self):
        classname = self.__class__.__name__
        return '{0}({1})'.format(classname, repr(self.url))

class ASF_WebsocketNotStarted(ASF_Error):

    pass
