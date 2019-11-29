import logging
from typing import Optional

import janus
from skpy import SkypeEventLoop as SkypeIternalCycle, SkypeNewMessageEvent, SkypeSingleChat
from .exceptions import StopSkypeLoopException
from settings import SKYPE_CREDENTIALS, SKYPE_TOKEN_PATH

log = logging.getLogger(__name__)


# Everything here works in synchronous mode
class SkypeEventSource(SkypeIternalCycle):
    def __init__(self):
        self.queue: Optional[janus._SyncQueueProxy] = None
        super().__init__(
            user=SKYPE_CREDENTIALS['login'],
            pwd=SKYPE_CREDENTIALS['password'],
            tokenFile=SKYPE_TOKEN_PATH
        )

    def loop(self):
        try:
            super().loop()
        except StopSkypeLoopException as ssle:
            self.queue.put(ssle)
            self.queue.join()
        except Exception as ex:
            log.error(str(ex))

    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent):
            if isinstance(self.chats[event.msg.chatId], SkypeSingleChat):
                self.queue.put(event)
                self.queue.join()
