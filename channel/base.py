from aiohttp import web
from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
from enum import Enum
from typing import Optional, List, Any

from app import app
from background.decorators import CRON_TASK, DATE_TASK, APTask
from channel.contacts import AddressBook, Contact
from channel.text_decorations import DefaultFormatter, TextNode
from database.models import AbstractUser


class TimeSpecifier(Enum):
    NEXT = 'next'
    EVERY = 'every'
    THIS = 'this'


@dataclass
class Schedule:
    datetime: datetime
    specifier: Optional[TimeSpecifier]

    @property
    def date(self) -> date:
        return self.exact_date.date()

    @property
    def exact_date(self) -> datetime:
        if self.specifier == TimeSpecifier.NEXT:
            return self.datetime + timedelta(weeks=1)
        return self.datetime

    @property
    def is_repetitive(self) -> bool:
        return self.specifier == TimeSpecifier.EVERY

    @property
    def time(self) -> time:
        return self.datetime.time()

    @property
    def day_of_week(self) -> str:
        return self.date.strftime("%A")


class BaseMessage(object):
    def __init__(self, channel: 'BaseChannel'):
        self.channel = channel

    async def reply(self, reply: TextNode):
        raise NotImplementedError()

    def text(self) -> List[str]:
        raise NotImplementedError()

    async def get_user(self) -> AbstractUser:
        return AbstractUser()


class BaseChannel(object):
    formatter = DefaultFormatter
    address_book: AddressBook

    def serialize_channel(self) -> str:
        return str(self)

    @staticmethod
    def deserialize_channel(app: web.Application, channel_id: str) -> Any:
        return app['channels'][channel_id]

    async def prepare(self):
        raise NotImplementedError()

    @staticmethod
    async def _send_formatted(chan_id, text: str, recipients: List[str]):
        channel = BaseChannel.deserialize_channel(app, chan_id)
        contacts = [channel.msg.channel.address_book.find_contact(c_id)
                    for c_id in recipients]
        return await channel.send_formatted(text, contacts)

    async def send_formatted(self, text: str, recipients: List[Contact]):
        raise NotImplementedError()

    async def schedule_send(self,
                            msg_text: TextNode,
                            recipients: List[Contact],
                            params: Schedule):
        text = self.format(msg_text)
        if params.is_repetitive:
            _type = CRON_TASK
            _schedule = {'cron_rule': None}
        else:
            _type = DATE_TASK
            _schedule = {'run_datetime': params.exact_date}
        task = APTask(_type, self._send_formatted)
        await task.start(
            kwargs={
                'chan_id': self.serialize_channel(),
                'text': text,
                'recipients': [r.id() for r in recipients],
            }, **_schedule
        )

    async def send(self, msg_text: TextNode, to: Contact):
        text = self.formatter().format(msg_text)
        await self.send_formatted(text, [to])

    def format(self, text: TextNode) -> str:
        formatter = self.formatter()
        return formatter.format(text)


class DummyContact(Contact):
    def __init__(self, term: str):
        self.term = term


class DummyAddressBook(AddressBook):
    def find_contact(self, search_term):
        return DummyContact(search_term)


class DummyChannel(BaseChannel):
    reply_: str
    contacts_: List[Contact]
    address_book = DummyAddressBook()

    async def prepare(self):
        pass

    async def send_formatted(self, text: str, recipients: List[Contact]):
        self.reply_ = text
        self.contacts_ = recipients


class DummyMessage(BaseMessage):
    def __init__(self, text: str):
        super().__init__(DummyChannel())
        self._text = text
        self.reply_: Optional[str] = None

    async def reply(self, reply: TextNode):
        await self.channel.send(reply, to=Contact())

    def text(self):
        return [t for t in map(str.strip, self._text.split(' ')) if t]
