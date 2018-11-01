import pyswagger

from . import utils


class IPC:

    def __init__(self, ipc='http://127.0.0.1:1242/', password='', timeout=5):
        self.ipc = ipc
        self.password = password
        self.timeout = timeout
        self.swagger = pyswagger.App.create(utils.build_url(ipc, '/swagger/ASF/swagger.json'))


class Endpoint:
    pass
