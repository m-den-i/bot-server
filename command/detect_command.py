from typing import Dict, List, Type, Iterable

from channel import BaseMessage
from channel.text_decorations import TextNode
from command.base import Command, CommandException
from conversation.base import Conversation


class DetectCommandConversation(Conversation):
    def __init__(self, command_classes: List[Type[Command]]):
        self.commands: Dict[str, Command] = {}
        self._init_commands(command_classes)

    async def react(self, msg: BaseMessage) -> None:
        reply = None
        sentence = msg.text()
        if len(sentence):
            command_name = sentence[0].lower()
            command_input = ' '.join(sentence[1:])
            if command_name in self.commands:
                try:
                    user = await msg.get_user()
                    if user.is_admin():
                        reply = await self.commands[command_name].execute(
                            command_input=command_input,
                            message=msg,
                        )
                except CommandException as e:
                    reply = str(e)
        if reply:
            await msg.reply(reply=TextNode(reply))

    def _init_commands(self, command_classes: Iterable[Type[Command]]):
        for cls in command_classes:
            command = cls()
            names = command.get_names()

            for name in names:
                if name in self.commands:
                    raise RuntimeError(
                        'Command with name {name} already exists. '
                        'Please, choose another one'.format(name=name)
                    )
                self.commands[name] = command
