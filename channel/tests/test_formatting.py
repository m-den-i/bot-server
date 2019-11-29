from channel.text_decorations import TextNode as t, HTMLFormatter


def test_formatting():
    formatter = HTMLFormatter()
    text_to_test = (
        "<b>Header</b>.<br>"
        "<b>Line: <i>1</i></b><br>"
        "Line: 2<br>"
        "Line: 3"
    )
    text_structure = t(
        t(t('Header').b(), '.').br(),
        t('Line: ', t('1').i()).b().br(),
        t('Line: 2').br(),
        'Line: 3',
    )
    assert text_to_test == formatter.format(text_structure)
