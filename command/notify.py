import re
from typing import List

from dateparser import parse

from background.scheduler import scheduler
from channel import BaseMessage
from channel.base import Schedule, TimeSpecifier
from channel.exceptions import ContactNotFoundException
from channel.text_decorations import TextNode as t
from command.base import Command, CommandException

EX_1 = "nfy next monday at 11:00 to John Doe with please check " \
       "your inbox\n"
EX_2 = "nfy 15.12.2019 at 03:00 PM to Jane Doe with send your CV"
EXCEPTION_MESSAGES = {
    'not_recognized': 'Could not recognize {entity} "{value}"',
    'invalid_format': (
            "Please, provide all necessary input args for command.:\n"
            "Examples:" + '\n{}\n{}'.format(EX_1, EX_2)
    )
}


class NotifyCommand(Command):
    NEXT = 'NEXT'
    EVERY = 'EVERY'
    THIS = 'THIS'

    SHOW = 'SHOW'
    CANCEL = 'CANCEL'

    create_pattern = re.compile(
        r'((([Oo]n)?(?P<day_of_week_adjective>next|this|every) '
        r'(?P<day_of_week>[a-zA-Z]+))|(?P<certain_date>.+)) '
        r'at (?P<certain_time>[0-9]{1,2}[\:\._][0-9]{2}\ ?(AM|PM)?) '
        r'(to )?(?P<receivers>.+) with (?P<msg>.+)'
    )

    async def execute(self, command_input, message):
        first_token = command_input.split(' ')[0].upper()

        if first_token in self.SHOW:
            return await self.show_notifications(command_input=command_input, message=message)
        elif first_token in self.CANCEL:
            return await self.cancel_notification(command_input=command_input, message=message)
        else:
            return await self.create_notification(command_input=command_input, message=message)

    def get_names(self) -> list:
        return [
            'notify', 'nfy'
        ]

    async def create_notification(self, command_input: str, message: BaseMessage):
        args = self.get_creation_params(command_input)
        return await self.set_notification(message, *args)

    async def show_notifications(self, command_input: str, message: BaseMessage):
        rows = []

        for j in scheduler.get_jobs():
            state = j.__getstate__()
            kwargs = state.get('kwargs')

            id = state['id']
            text = kwargs['text']
            recipients = ','.join(kwargs['recipients']) or '-'
            next_run_time = state.get('next_run_time')
            is_repetitive = 'No' if state.get('trigger').__slots__ == 'run_date' else 'Yes'

            _date = next_run_time.strftime('%d.%m.%Y')
            _day_of_week = next_run_time.strftime('%A')
            _time = next_run_time.strftime('%H:%M')

            rows.append(t(
                *(
                    t(F'ID: {id}').br(),
                    t(F'Text: {text}').br(),
                    t(F'Recipients: {recipients}').br(),
                    t(F'Datetime/DOW: {_date} {_time} / {_day_of_week}').br(),
                    t(F'Is repetitive: {is_repetitive}').br(),
                )
            ).br())

        return t(*rows) if len(rows) > 0 else 'There are no notify tasks'

    async def cancel_notification(self, command_input: str, message: BaseMessage):
        parts = message.text()

        if len(parts) <= 2:
            raise CommandException('Please, specify ID of notify task! Send command in format: nfy cancel {task_id}')

        job_id = parts[2]
        job = scheduler.get_job(job_id=job_id)

        if job:
            job.remove()

            return F'Task with ID {job_id} successfully cancelled'

        raise CommandException(F'Task with ID {job_id} not found')

    def get_creation_params(self, input_str: str) -> (t, Schedule):
        matches = self.create_pattern.match(input_str)
        if not matches:
            raise CommandException(EXCEPTION_MESSAGES['invalid_format'])
        parsed = matches.groupdict()
        day_of_week_adjective = parsed.get('day_of_week_adjective', None)

        if day_of_week_adjective:
            day_of_week_adjective = day_of_week_adjective.upper()
            _datetime = parse(parsed['day_of_week'])
            if not _datetime:
                CommandException(
                    EXCEPTION_MESSAGES['not_recognized'].format(
                        entity='day of week',
                        value=parsed['day_of_week'],
                    )
                )
            if day_of_week_adjective not in (self.NEXT, self.THIS, self.EVERY):
                raise CommandException('Unknown period specifier.')
            specifier = TimeSpecifier[day_of_week_adjective]
        else:
            specifier = None
            _datetime = parse(parsed['certain_date'])
            if not _datetime:
                raise CommandException(
                    EXCEPTION_MESSAGES['not_recognized'].format(
                        entity='date',
                        value=parsed['certain_date'],
                    )
                )

        _time = parse(parsed['certain_time'])
        if not _time:
            raise CommandException(
                EXCEPTION_MESSAGES['not_recognized'].format(
                    entity='time',
                    value=parsed['certain_time'],
                ),
            )
        _time = _time.time()
        _datetime = _datetime.replace(
            hour=_time.hour,
            minute=_time.minute,
        )
        return (
            t(parsed['msg']),
            parsed['receivers'].split(','),
            Schedule(
                datetime=_datetime,
                specifier=specifier,
            ),
        )

    async def set_notification(self,
                               msg: BaseMessage,
                               msg_text: t,
                               receivers: List[str],
                               params: Schedule):

        recipients = []

        for r in receivers:
            try:
                recipients.append(msg.channel.address_book.find_contact(r))
            except ContactNotFoundException as e:
                raise CommandException(str(e))

        await msg.channel.schedule_send(
            msg_text=msg_text,
            recipients=recipients,
            params=params,
        )
        if params.is_repetitive:
            when_t = t(F'every {params.day_of_week.capitalize()}')
        else:
            when_t = t(params.date.strftime('%d.%m.%Y'))
        return t(*(
            t('When: ', when_t.b()).br(),
            t('Time: ', t(params.time.strftime('%H:%M')).b()).br(),
            t('Receivers: ', t(','.join(receivers)).b()).br(),
            t('Message: ', msg_text.b()),
        ))
