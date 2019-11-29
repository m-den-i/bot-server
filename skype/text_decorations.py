from skpy import SkypeMsg

from channel.text_decorations import DefaultFormatter, Tag


class SkypeFormatter(DefaultFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rules.update({
            Tag.BOLD: SkypeMsg.bold,
            Tag.ITALIC: SkypeMsg.italic,
        })
