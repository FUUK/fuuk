"""
Unittests for templatetags
"""
import unittest

from django.template import Context, Template
from django.test import SimpleTestCase
from django.utils.html import conditional_escape

from fuuk.common.templatetags.markup import markdown, textile


class TestTextile(unittest.TestCase):
    """
    Unittest of `textile` filter.
    """
    def test_call(self):
        self.assertEqual(textile('*Textile* _test_'), '\t<p><strong>Textile</strong> <em>test</em></p>')
        # Non-string argument
        self.assertEqual(textile(None), '\t<p>None</p>')

        # Don't escape existing HTML
        self.assertEqual(textile('<b>Text</b>'), '\t<p><b>Text</b></p>')

    def test_render(self):
        template = Template('{% load markup %}{{ value|textile }}')
        context = Context({'value': '*Textile* _test_'})
        self.assertEqual(template.render(context), '\t<p><strong>Textile</strong> <em>test</em></p>')


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
