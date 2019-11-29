from channel import BaseMessage
from channel.text_decorations import TextNode


class Command(object):
    async def execute(self, command_input: str, message: BaseMessage) \
            -> TextNode:
        raise NotImplementedError()

    def get_names(self) -> list:
        raise NotImplementedError()


class CommandException(Exception):
    pass
