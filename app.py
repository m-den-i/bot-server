from aiohttp import web

from database.manager import database_manager
from loop import event_loop, executor


app = web.Application(loop=event_loop)
app['loop'] = event_loop
app['executor'] = executor
app['db_manager'] = database_manager
