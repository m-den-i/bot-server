from channel import BaseMessage


class Conversation(object):
    async def react(self, msg: BaseMessage) -> None:
        raise NotImplementedError()
