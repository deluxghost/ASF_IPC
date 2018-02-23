# -*- coding: utf-8 -*-
import asyncio
import posixpath
import urllib.parse as urlparse
import requests
import websockets

from . import error
from . import response

__version__ = '1.1.3'
ALLBOT = 'ASF'


class IPC(object):

    def __init__(self, ipc='http://127.0.0.1:1242/', password='', timeout=5):
        self.ipc = ipc
        self.password = password
        self.timeout = timeout
        self.wslog = None

    @classmethod
    def _botjoin(cls, bots):
        botnames = bots
        if isinstance(botnames, (list, tuple, set)):
            botnames = ','.join(botnames)
        return botnames

    def _add_auth(self, headers=None):
        if headers is None:
            auth_headers = dict()
        else:
            auth_headers = headers
        if self.password:
            auth_headers['Authentication'] = self.password
        return auth_headers

    def _build_endpoint(self, endpoint, keyword=None, ws=False):
        ipc_split = list(urlparse.urlsplit(self.ipc))
        ipc_split[2] = posixpath.join(ipc_split[2], 'Api', endpoint)
        if keyword:
            keyword = urlparse.quote_plus(keyword)
            ipc_split[2] = posixpath.join(ipc_split[2], keyword)
        if ws and ipc_split[0] == 'http':
            ipc_split[0] = 'ws'
        elif ws and ipc_split[0] == 'https':
            ipc_split[0] = 'wss'
        return urlparse.urlunsplit(ipc_split)

    def get(self, endpoint, keyword=None, headers=None):
        url = self._build_endpoint(endpoint, keyword)
        headers = self._add_auth(headers)
        try:
            resp = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            raise error.ASF_ConnectionError(url)
        resp = response.GenericResponse(resp)
        return resp.result

    def delete(self, endpoint, keyword=None, headers=None):
        url = self._build_endpoint(endpoint, keyword)
        headers = self._add_auth(headers)
        try:
            resp = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            raise error.ASF_ConnectionError(url)
        resp = response.GenericResponse(resp)
        return resp.result

    def post(self, endpoint, keyword=None, headers=None, body=None, is_json=False):
        url = self._build_endpoint(endpoint, keyword)
        headers = self._add_auth(headers)
        try:
            if is_json:
                headers['Content-Type'] = 'application/json'
                resp = requests.post(url, json=body, headers=headers, timeout=self.timeout)
            else:
                resp = requests.post(url, data=body, headers=headers, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            raise error.ASF_ConnectionError(url)
        resp = response.GenericResponse(resp)
        return resp.result

    def post_json(self, endpoint, keyword=None, headers=None, body=None):
        return self.post(endpoint, keyword, headers, body, is_json=True)

    def get_asf(self):
        return self.get('ASF')

    def post_asf(self, global_config, **kwargs):
        payload = {
            'GlobalConfig': global_config
        }
        for key, value in kwargs.items():
            payload[key] = value
        return self.post_json('ASF', body=payload)

    def get_bot(self, botnames):
        botnames = self._botjoin(botnames)
        return self.get('Bot', botnames)

    def delete_bot(self, botnames):
        botnames = self._botjoin(botnames)
        return self.delete('Bot', botnames)

    def post_bot(self, botname, bot_config, **kwargs):
        payload = {
            'BotConfig': bot_config,
            'KeepSensitiveDetails': True
        }
        for key, value in kwargs.items():
            payload[key] = value
        return self.post_json('Bot', botname, body=payload)

    def get_command(self, cmd):
        return self.get('Command', cmd)

    def post_command(self, cmd):
        return self.post('Command', cmd)

    def command(self, cmd):
        return self.post_command(cmd)

    def get_structure(self, structure_name):
        return self.get('Structure', structure_name)

    def get_type(self, type_name):
        return self.get('Type', type_name)

    def post_games_to_redeem_in_background(self, botname, games, **kwargs):
        payload = {
            'GamesToRedeemInBackground': games
        }
        for key, value in kwargs.items():
            payload[key] = value
        return self.post_json('GamesToRedeemInBackground', botname, body=payload)

    async def start_log(self):
        await self.stop_log()
        ws_url = self._build_endpoint('Log', ws=True)
        headers = self._add_auth()
        self.wslog = websockets.connect(ws_url, extra_headers=headers)

    async def stop_log(self):
        if self.wslog is None:
            return
        await self.wslog.ws_client.close()
        self.wslog = None

    async def get_log(self):
        if self.wslog is None:
            raise error.ASF_WebsocketNotStarted('Websocket client isn\'t started, try `start_log()` first?')
        async with self.wslog as websocket:
            while True:
                try:
                    resp = await websocket.recv()
                    resp = response.WebsocketResponse(resp)
                    yield resp.result
                except websockets.exceptions.ConnectionClosed:
                    yield None
