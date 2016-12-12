from django.test import SimpleTestCase

from fuuk.common.forms import get_markdown_help_text


class TestGetMarkdownHelpText(SimpleTestCase):
    """
    Test `get_markdown_help_text` function.
    """
    def test_call(self):
        result = 'This field uses <a href="https://daringfireball.net/projects/markdown/" target="_blank">' \
                 'Markdown language</a> with ' \
                 '<a href="https://pythonhosted.org/Markdown/extensions/tables.html" target="_blank">tables</a> and ' \
                 '<a href="https://pythonhosted.org/Markdown/extensions/attr_list.html" target="_blank">attr_list</a>' \
                 ' extensions.'
        self.assertEqual(get_markdown_help_text(), result)
