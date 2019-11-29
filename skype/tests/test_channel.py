import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from skpy import SkypeConnection, SkypeNewMessageEvent

from skype.contacts import SkypeChannelContact
from ..channel import SkypeChannel
from ..exceptions import StopSkypeLoopException


async def async_pass(*args, **kwargs):
    pass


def always_successful_registration(token):
    def f(self):
        user, skypeToken, skypeExpiry, regToken, regExpiry, msgsHost = token
        self.userId = user
        self.tokens["skype"] = skypeToken
        self.tokenExpiry["skype"] = skypeExpiry
        if datetime.now() < regExpiry:
            self.tokens["reg"] = regToken
            self.tokenExpiry["reg"] = regExpiry
            self.msgsHost = msgsHost
        else:
            self.getRegToken()
    return f


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_channel_functional(skype_contacts,
                                  skype_chats,
                                  skype_mention,
                                  fake_token):
    fake_app = {
        'loop': asyncio.get_event_loop(),
        'executor': ThreadPoolExecutor(max_workers=3),
        'conversation': Mock(),
    }

    def event_generator():
        with patch.object(SkypeNewMessageEvent, 'ack') as fake_ack:
            yield skype_mention
        assert fake_ack.called_once()
        exc = StopSkypeLoopException()
        # Will close reading thread
        yield [exc]
        # Will close writing thread
        raise exc
    react_mock = Mock()
    fake_app['conversation'].react = react_mock
    react_mock.return_value = async_pass()

    events = event_generator()
    channel = SkypeChannel(fake_app)
    with patch.object(
            SkypeConnection,
            'readToken',
            always_successful_registration(fake_token),
    ):
        await channel.prepare()
    with patch.object(channel.skype_el, 'contacts', skype_contacts):
        with patch.object(channel.skype_el, 'chats', skype_chats):
            cont = channel.address_book.find_contact('test-skype-id')
    with patch.object(channel.skype_el, 'getEvents', lambda: next(events)):
        # Switch to other coroutines
        await channel.pipes[1]
        await channel.pipes[0]
    assert react_mock.call_args[0][0].sk_ev is skype_mention[0]
    assert isinstance(cont, SkypeChannelContact)
    assert cont.contact.id == 'test-skype-id'


@pytest.mark.asyncio
async def test_scheduled_send_works(db_manager):
    pass
