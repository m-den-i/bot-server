import logging

from aiohttp import WSMsgType, web, WSMessage
from aiohttp.abc import Request
from aiohttp.web_ws import WebSocketResponse

from channel import BaseChannel, BaseMessage

log = logging.getLogger(__name__)


class WebsocketChannel(BaseChannel):
    def __init__(self, app, route='/discussion'):
        self.app = app
        self.route = route
        for r, v in (
            (self.route, self.ws_handler),
        ):
            self.app.router.add_get(r, v)

    async def ws_handler(self, request: Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await self.app['conversation'].react(
                        WebsocketMessage(self, ws, msg)
                    )
            elif msg.type == WSMsgType.ERROR:
                log.error('ws connection closed with exception %s' %
                          ws.exception())
        log.error('websocket connection closed')
        return ws

    async def prepare(self, *args, **kwargs):
        pass


class WebsocketMessage(BaseMessage):
    def __init__(self,
                 channel: BaseChannel,
                 ws_conn: WebSocketResponse,
                 ws_msg: WSMessage):
        super().__init__(channel)
        self.ws_conn = ws_conn
        self.ws_msg = ws_msg

    async def reply(self, reply):
        text = self.channel.format(reply)
        await self.ws_conn.send_str(text)

    def text(self):
        msg = self.ws_msg
        sentence = [m for m in map(str.strip, msg.data.split(' '))
                    if m != '']
        return sentence
