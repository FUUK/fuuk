# -*- coding: utf-8 -*-
'''
Unittests for utils.
'''
from django.test import SimpleTestCase

from fuuk.people.utils import full_name, sanitize_filename


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


class TestFullName(SimpleTestCase):
    """
    Test `full_name` function.
    """
    def test_full_name(self):
        self.assertEqual(full_name('RNDr.', 'Pepa', 'Jahoda', 'PhD.'),
                         'RNDr. Pepa Jahoda, PhD.')
        self.assertEqual(full_name(None, 'Pepa', 'Jahoda', None),
                         'Pepa Jahoda')
        self.assertEqual(full_name(None, u'Někdo', u'Hruška', None),
                         u'Někdo Hruška')
        self.assertEqual(full_name(None, 'Pepa', 'Jahoda', ''),
                         u'Pepa Jahoda')
        self.assertEqual(full_name('Prof. Mgr. et Bc.', 'Pepa', 'Jahoda', None),
                         'Prof. Mgr. et Bc. Pepa Jahoda')
        self.assertEqual(full_name('', 'Pepa', 'Jahoda', None),
                         'Pepa Jahoda')
