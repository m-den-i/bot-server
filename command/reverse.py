from channel.text_decorations import TextNode
from command.base import Command


class ReverseCommand(Command):
    async def execute(self, command_input, message):
        return TextNode(''.join(reversed(command_input)))

    def get_names(self) -> list:
        return [
            'reverse', 'rvs'
        ]
