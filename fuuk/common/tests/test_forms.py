from django.test import SimpleTestCase

from fuuk.common.forms import get_markdown_help_text


class TestGetMarkdownHelpText(SimpleTestCase):
    """
    Test `get_markdown_help_text` function.
    """
    def test_call(self):
        result = '<a href="https://daringfireball.net/projects/markdown/" target="_blank">' \
                 'This field uses Markdown language.</a>'
        self.assertEqual(get_markdown_help_text(), result)
