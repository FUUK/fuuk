"""
Unittests for templatetags
"""
import unittest

from django.template import Context, Template

from fuuk.common.templatetags.markup import textile


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
