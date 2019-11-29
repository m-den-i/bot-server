#!/usr/bin/env python
import logging
import os
import sys
import time

from aiohttp import web

from app import app
from background.scheduler import scheduler
from command.detect_command import DetectCommandConversation
from command.notify import NotifyCommand
from command.reverse import ReverseCommand
from loop import event_loop
from routes import setup_routes
import settings
from skype.channel import SkypeChannel
from websocket.channel import WebsocketChannel

# Timezone
os.environ['TZ'] = settings.TIMEZONE
time.tzset()

# DB
app.on_startup.append(app['db_manager'].connect)
app.on_shutdown.append(app['db_manager'].disconnect)

# Routes
setup_routes(app)

if settings.DEBUG:
    CHANNELS = [WebsocketChannel]
    if settings.USE_SKYPE:
        CHANNELS.append(SkypeChannel)
    event_loop.set_debug(True)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )
else:
    CHANNELS = [WebsocketChannel, SkypeChannel]
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

# Channels and conversations
app['channels'] = {}
for ch in (cl(app) for cl in CHANNELS):
    app['channels'][str(ch)] = ch
    app.on_startup.append(ch.prepare)
app['conversation'] = DetectCommandConversation([
    ReverseCommand,
    NotifyCommand,
])

scheduler.start()

if settings.DEBUG:
    import aiohttp_autoreload

    aiohttp_autoreload.start()

web.run_app(app, host=settings.APP['host'], port=settings.APP['port'])
