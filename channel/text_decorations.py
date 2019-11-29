from typing import Dict, Callable, Tuple, Union


class TextNode:
    def __init__(self, *children: Union['TextNode', str], text=''):
        self.tags: Tuple = ()
        self.text: str = text
        self.children: Tuple[TextNode] = tuple(
            TextNode(text=ch) if isinstance(ch, str) else ch for ch in children
        )

    def b(self):
        self.tags += (Tag.BOLD,)
        return self

    def i(self):
        self.tags += (Tag.ITALIC,)
        return self

    def q(self):
        self.tags += (Tag.QUOTED,)
        return self

    def br(self):
        self.tags += (Tag.LINE,)
        return self


class Tag:
    LINE = 1
    BOLD = 2
    ITALIC = 3
    QUOTED = 4


class DefaultFormatter:
    def __init__(self):
        self.rules: Dict[int, Callable[[str], str]] = {
            Tag.LINE: '{}\n'.format,
            Tag.BOLD: self.text,
            Tag.ITALIC: self.text,
            Tag.QUOTED: '"{}"'.format,
            None: self.text
        }

    @classmethod
    def text(cls, text: str) -> str:
        return text

    def format(self, root: TextNode):
        stack: Tuple[TextNode] = (root,)
        heads = ()
        while stack:
            if stack[0].children:
                if heads and stack[0] is heads[0]:
                    # We are returning back, all children are visited
                    head, *heads = heads
                    head.children = None
                    # Next iteration will pop the node
                    continue
                # Or go left deeper
                heads = (stack[0], *heads)
                stack = stack[0].children + stack
            else:
                # Pop leaves and wrap their content into decorations
                node, stack = stack[0], stack[1:]
                _f_text = node.text
                for tag_name in node.tags:
                    _f_text = self.rules[tag_name](_f_text)
                if heads:
                    heads[0].text += _f_text
        return root.text


class HTMLFormatter(DefaultFormatter):
    def __init__(self):
        super().__init__()
        self.rules.update({
            Tag.BOLD: '<b>{}</b>'.format,
            Tag.ITALIC: '<i>{}</i>'.format,
            Tag.LINE: '{}<br>'.format,
            None: self.text
        })
