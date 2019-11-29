from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dateutil import parser

from channel.base import DummyMessage
from command.detect_command import DetectCommandConversation
from command.notify import EX_1, EX_2, NotifyCommand
from command.reverse import ReverseCommand


# All test are asyncio coroutines
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("_msg,_reply", [
    ('Reverse ABC', 'CBA'),
    ('rvs Text to go', 'og ot txeT'),
    ('Reverse Дон Карлеоне', 'еноелраК ноД'),
])
async def test_rvs_command(_msg: str, _reply: str):
    conversation = DetectCommandConversation([ReverseCommand])
    msg = DummyMessage(_msg)
    await conversation.react(msg)
    assert msg.channel.reply_ == _reply


next_mon = datetime.now()
next_mon = (next_mon - timedelta(days=next_mon.weekday())) + timedelta(weeks=1)


@pytest.mark.parametrize("_msg,_rpl", [
    ('Notify 10 Jan at 12.00 test-skype-id with Eat your pill',
     'When: 10.01.2019\n'
     'Time: 00:00\n'
     'Receivers: test-skype-id\n'
     'Message: Eat your pill'),
    (EX_1,
     'When: ' + next_mon.strftime('%d.%m.%Y') + '\n'
     'Time: 11:00\n'
     'Receivers: John Doe\n'
     'Message: please check your inbox'),
    (EX_2,
     'When: 15.12.2019\n'
     'Time: 15:00\n'
     'Receivers: Jane Doe\n'
     'Message: send your CV'),
])
async def test_notify_command(_msg: str, _rpl: str):
    conversation = DetectCommandConversation([NotifyCommand])
    msg = DummyMessage(_msg)
    with patch.object(AsyncIOScheduler, 'add_job') as fake_job:
        await conversation.react(msg)
    assert msg.channel.reply_ == _rpl
    txt_dict = dict(ln.split(': ') for ln in _rpl.split('\n'))
    who = [msg.channel.address_book.find_contact(r)
           for r in txt_dict['Receivers'].split(',')]
    assert fake_job.called_with(
        msg.channel.send_formatted,
        args=(),
        kwargs={
            'text': txt_dict['Message'],
            'recipients': who,
        },
        id=None,
        name=None,
        run_date=parser.parse(
            '{} {}'.format(txt_dict['When'], txt_dict['Time'])
        )
    )
