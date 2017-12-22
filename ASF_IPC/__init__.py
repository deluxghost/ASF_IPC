# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import requests

from . import response

ALLBOT = 'ASF'


class IPC(object):

    def __init__(self, host='127.0.0.1', port=1242, password='', timeout=5):
        self.host = host
        self.port = port
        self.password = password
        self.root_url = 'http://{0}:{1}'.format(host, port)
        self.timeout = timeout

    @classmethod
    def _botjoin(cls, bots):
        botnames = bots
        if isinstance(botnames, (list, tuple)):
            botnames = ','.join(botnames)
        botnames = urlparse.quote_plus(botnames)
        return botnames

    def _add_auth(self, headers=None):
        if headers is None:
            auth_headers = dict()
        else:
            auth_headers = headers
        if self.password:
            auth_headers['Authentication'] = self.password
        return auth_headers

    def _get(self, url, headers=None):
        headers = self._add_auth(headers)
        resp = requests.get(url, headers=headers, timeout=self.timeout)
        resp = response.GenericResponse(resp)
        if not resp.success:
            raise Exception(resp.error)
        return resp.result

    def _delete(self, url, headers=None):
        headers = self._add_auth(headers)
        resp = requests.delete(url, headers=headers, timeout=self.timeout)
        resp = response.GenericResponse(resp)
        if not resp.success:
            raise Exception(resp.error)

    def _post(self, url, data=None, headers=None):
        headers = self._add_auth(headers)
        resp = requests.post(url, json=data, headers=headers, timeout=self.timeout)
        resp = response.GenericResponse(resp)
        if not resp.success:
            raise Exception(resp.error)
        return resp.result

    def get_bot(self, botnames, key=None):
        botnames = self._botjoin(botnames)
        address = self.root_url + '/Api/Bot/' + botnames
        return self._get(address)

    def delete_bot(self, botnames):
        botnames = self._botjoin(botnames)
        address = self.root_url + '/Api/Bot/' + botnames
        self._delete(address)

    def post_bot(self, botname, config, keep_sensitive=True):
        botname = urlparse.quote_plus(botname)
        address = self.root_url + '/Api/Bot/' + botname
        headers = {'Content-Type': 'application/json'}
        payload = {
            'BotConfig': config,
            'KeepSensitiveDetails': keep_sensitive
        }
        self._post(address, payload, headers)

    def command(self, cmd):
        cmd = urlparse.quote_plus(cmd)
        address = self.root_url + '/Api/Command/' + cmd
        return self._post(address)

    def get_structure(self, name):
        name = urlparse.quote_plus(name)
        address = self.root_url + '/Api/Structure/' + name
        return self._get(address)

    def get_type(self, name):
        name = urlparse.quote_plus(name)
        address = self.root_url + '/Api/Type/' + name
        return self._get(address)
