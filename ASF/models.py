import aiohttp
import pyswagger

from . import utils


class IPC:

    def __init__(self, ipc='http://127.0.0.1:1242/', password='', timeout=5):
        self._ipc = ipc
        self._password = password
        self._timeout = timeout

    async def __aenter__(self):
        self._swagger = pyswagger.App.create(utils.build_url(self._ipc, '/swagger/ASF/swagger.json'))
        for api in self._swagger.op.values():
            p = self
            p_path = ''
            for node in api.path.strip(utils.sep).split(utils.sep):
                p_path += f'/{node}'
                if node.startswith('{') and node.endswith('}'):
                    arg = node[1:-1]
                    p._append(self, arg)
                    p = p[arg]
                else:
                    if not hasattr(p, node):
                        setattr(p, node, Endpoint(self))
                    p = getattr(p, node)
                p._path = p_path
        headers = dict()
        if self._password:
            headers['Authentication'] = self._password
        timeout = aiohttp.ClientTimeout(total=self._timeout)
        self._session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()


class Endpoint:

    def __init__(self, ipc):
        self._kw = dict()
        self._path = None
        self._ipc = ipc

    def __getitem__(self, key):
        return self._kw[key]

    def _append(self, ipc, kw):
        if kw not in self._kw:
            self._kw[kw] = Endpoint(ipc)

    async def _request(self, method, body=None, params=None, **kw):
        session = self._ipc._session
        url = utils.build_url(self._ipc._ipc, self._path)
        for k, v in kw.items():
            url = url.replace(f'{{{k}}}', utils.quote(v))
        async with session.request(method, url, json=body, params=params) as resp:
            try:
                json_data = await resp.json()
            except Exception:
                json_data = None
            text = await resp.text()
            return ASFResponse(resp, json_data, text)

    async def ws(self, **kw):
        session = self._ipc._session
        url = utils.build_url(self._ipc._ipc, self._path)
        for k, v in kw.items():
            url = url.replace(f'{{{k}}}', utils.quote(v))
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        json_data = msg.json()
                    except Exception:
                        json_data = None
                    text = msg.data
                    yield WSResponse(url, json_data, text)
                elif msg.type == aiohttp.WSMsgType.ERROR or msg.type == aiohttp.WSMsgType.CLOSE:
                    break

    async def get(self, **kw):
        return await self._request('get', **kw)

    async def post(self, **kw):
        return await self._request('post', **kw)

    async def put(self, **kw):
        return await self._request('put', **kw)

    async def delete(self, **kw):
        return await self._request('delete', **kw)


class WSResponse:

    def __init__(self, url, json_data, text):
        self.url = url
        if json_data:
            self.ok = True
            self.message = json_data.get('Message')
            self.result = json_data.get('Result')
            self.success = json_data.get('Success')
        else:
            self.ok = False
            self.message = text
            self.result = None
            self.success = False
        self.OK = self.ok
        self.Message = self.message
        self.Result = self.result
        self.Success = self.success


class ASFResponse:

    def __init__(self, resp, json_data, text):
        status = resp.status
        reason = resp.reason
        self.url = resp.url
        if json_data:
            self.ok = True
            self.message = json_data.get('Message')
            self.result = json_data.get('Result')
            self.success = json_data.get('Success')
        else:
            self.ok = False
            self.message = text if text else f'{status} - {reason}'
            self.result = None
            self.success = False
        self.OK = self.ok
        self.Message = self.message
        self.Result = self.result
        self.Success = self.success
