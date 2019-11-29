from asyncio import Task
from typing import List, Type

from aiohttp import web
import janus
from skpy import SkypeSingleChat

from channel import BaseChannel, BaseMessage
from channel.text_decorations import DefaultFormatter
from database.models import User, AbstractUser

from .contacts import SkypeAddressBook, SkypeChannelContact
from .event_source import SkypeEventSource
from .exceptions import StopSkypeLoopException
from .text_decorations import SkypeFormatter


class SkypeChannel(BaseChannel):
    formatter: Type[DefaultFormatter] = SkypeFormatter
    skype_el: SkypeEventSource
    pipes: List[Task]

    def __init__(self, app: web.Application):
        self.app = app
        self.queue = janus.Queue(loop=self.loop)
        self.pipes = []

    @property
    def loop(self):
        return self.app['loop']

    async def read_events(self):
        async_q = self.queue.async_q
        while True:
            ev = await async_q.get()
            async_q.task_done()
            if isinstance(ev, StopSkypeLoopException):
                break
            await self.app['conversation'].react(
                SkypeMessage(self, ev, self.loop)
            )

    async def send_formatted(self,
                             text,
                             recipients: List[SkypeChannelContact]):
        for r in recipients:
            await self.send_to_chat(r.contact.chat, text)

    async def send_to_chat(self, chat: SkypeSingleChat, text: str):
        await self.loop.run_in_executor(
            self.app.get('executor', None),
            lambda: chat.sendMsg(text, rich=True),
        )

    async def run_loop(self):
        await self.loop.run_in_executor(
            self.app.get('executor', None),
            self.skype_el.loop
        )

    async def prepare(self, *args, **kwargs):
        self.skype_el = await self.loop.run_in_executor(
            self.app.get('executor', None),
            lambda: SkypeEventSource(),
        )
        self.skype_el.queue = self.queue.sync_q
        await self.update_address_book()
        for t in (
                self.read_events(),
                self.run_loop()
        ):
            self.pipes.append(self.loop.create_task(t))

    async def update_address_book(self):
        self.address_book = await self.loop.run_in_executor(
            self.app.get('executor', None),
            lambda: SkypeAddressBook(
                self.skype_el.contacts,
                self.skype_el.chats,
            ),
        )


class SkypeMessage(BaseMessage):
    def __init__(self, channel, skype_event, loop):
        super().__init__(channel)
        self.sk_ev = skype_event
        self.loop = loop

    async def reply(self, reply):
        text = self.channel.format(reply)
        await self.channel.send_to_chat(self.sk_ev.msg.chat, text)

    def text(self) -> list:
        sentence = [m for m
                    in map(str.strip, self.sk_ev.msg.content.split(' '))
                    if m != '']
        return sentence

    async def get_user(self):
        skype_id = self.sk_ev.msg.userId

        users = await User.async_find_by(fields=['skype_id'], where_clauses=[
            User.skype_id == skype_id
        ])

        if len(users):
            return users[0]

        # User is unknown
        return AbstractUser()

        # TODO: raise exception unless user with skype_id exists in DB or
        #   check the user in SMG
        #   and if it's a newcomer, fetch this user from SMG and save into DB
