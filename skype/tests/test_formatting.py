from channel.text_decorations import TextNode as t
from skype.text_decorations import SkypeFormatter


def test_skype_formatting():
    formatter = SkypeFormatter()
    text_to_test = """When: <b raw_pre="*" raw_post="*">26.11.2019</b>
Time: <b raw_pre="*" raw_post="*">23:00</b>
Receivers: <b raw_pre="*" raw_post="*">Jane Doe</b>
Message: <b raw_pre="*" raw_post="*">check your inbox</b>"""
    text_structure = t(
        'When: ', t('26.11.2019').b().br(),
        'Time: ', t('23:00').b().br(),
        'Receivers: ', t('Jane Doe').b().br(),
        'Message: ', t('check your inbox').b(),
    )
    assert text_to_test == formatter.format(text_structure)
