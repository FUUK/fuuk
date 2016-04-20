# -*- coding: utf-8 -*-
'''
Unittests for utils.
'''
from django.test import SimpleTestCase

from fuuk.people.utils import sanitize_filename


class TestSanitizeFilename(SimpleTestCase):
    """
    Test `sanitize_filename` function.
    """
    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename('foo.dat'), 'foo.dat')
        self.assertEqual(sanitize_filename('foo.bar.dat'), 'foobar.dat')
        self.assertEqual(sanitize_filename('foo bar.dat'), 'foo-bar.dat')
        self.assertEqual(sanitize_filename('ěščřž.dat'), 'escrz.dat')
        self.assertEqual(sanitize_filename(u'ěščřž.dat'), 'escrz.dat')
        self.assertEqual(sanitize_filename('.dat'), 'dat')
        self.assertEqual(sanitize_filename('foo.dať'), 'foo.dat')

    def test_path(self):
        self.assertEqual(sanitize_filename('foo.dat'), 'foo.dat')
        self.assertEqual(sanitize_filename('foo.dat', ''), 'foo.dat')
        self.assertEqual(sanitize_filename('foo.dat', 'files/courses/'), 'files/courses/foo.dat')
        self.assertEqual(sanitize_filename('foo.dat', 'files/courses'), 'files/courses/foo.dat')
