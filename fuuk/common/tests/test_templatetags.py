"""
Unittests for templatetags
"""
from django.test import SimpleTestCase
from django.utils.html import conditional_escape

from fuuk.common.templatetags.markup import markdown


class TestMarkdown(SimpleTestCase):
    """
    Test `markdown` filter.
    """
    def test_filter(self):
        self.assertEqual(markdown(None), '<p>None</p>')
        self.assertEqual(markdown(''), '')
        self.assertEqual(markdown('<div>text</div>'), '<div>text</div>')
        self.assertEqual(markdown('### Header ###\n\nParagraph.'), '<h3>Header</h3>\n<p>Paragraph.</p>')

    def test_safe_output(self):
        output = markdown('<div>text</div>')
        self.assertEqual(conditional_escape(output), output)
