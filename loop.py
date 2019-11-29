import asyncio
from concurrent.futures import ThreadPoolExecutor

import uvloop

import settings

event_loop = uvloop.new_event_loop()
executor = ThreadPoolExecutor(max_workers=settings.THREAD_POOL)

event_loop.set_default_executor(executor)
asyncio.set_event_loop(event_loop)
