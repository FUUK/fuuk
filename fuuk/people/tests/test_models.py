# -*- coding: utf-8 -*-
"""
Tests of models.
"""
import os.path
import unittest
from shutil import rmtree
from tempfile import mkdtemp

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase, TestCase
from mock import patch, sentinel

from fuuk.people.models.article import doi_validator
from fuuk.people.models.course import Attachment, attachment_filename, Course
from fuuk.people.models.person import Person


class TestValidators(unittest.TestCase):
    """
    Unittests for validators.
    """
    def test_doi_validator(self):
        doi_validator('10.1000')
        doi_validator('10.1000/182')
        self.assertRaises(ValidationError, doi_validator, 'not a doi')
        # We don't allow the doi prefix itself
        self.assertRaises(ValidationError, doi_validator, 'doi:10.1000')


class TestPersonName(unittest.TestCase):
    """
    Unittests for name and name_reversed @property on Person model
    """
    def test_name(self):
        A = Person.objects.create(last_name="Tester", first_name="Bad Name  ", prefix=" Mgr.  ")
        self.assertEqual(A.name, 'Tester B.N.')
        self.assertEqual(A.name_reversed, 'B.N. Tester')
        self.assertEqual(A.full_name, 'Mgr. Bad Name Tester')
        A = Person.objects.create(last_name="Tester", first_name="  Second Bad Name ", suffix=" RNDr.")
        self.assertEqual(A.name, 'Tester S.B.N.')
        self.assertEqual(A.name_reversed, 'S.B.N. Tester')
        self.assertEqual(A.full_name, 'Second Bad Name Tester, RNDr.')
        A = Person.objects.create(last_name="Tester", first_name="Bad With  Spaces ")
        self.assertEqual(A.name, 'Tester B.W.S.')
        self.assertEqual(A.name_reversed, 'B.W.S. Tester')
        self.assertEqual(A.full_name, 'Bad With Spaces Tester')


class TestAttachmentFilename(SimpleTestCase):
    """
    Test `attachment_filename` function.
    """
    def test_attachment_filename(self):
        # Test `attachment_filename` function
        self.assertEqual(attachment_filename(sentinel.instance, 'foo.dat'), 'files/courses/foo.dat')
        self.assertEqual(attachment_filename(sentinel.instance, 'foo.bar.dat'), 'files/courses/foobar.dat')
        self.assertEqual(attachment_filename(sentinel.instance, 'foo bar.dat'), 'files/courses/foo-bar.dat')
        self.assertEqual(attachment_filename(sentinel.instance, 'ěščřž.dat'), 'files/courses/escrz.dat')
        self.assertEqual(attachment_filename(sentinel.instance, u'ěščřž.dat'), 'files/courses/escrz.dat')
        self.assertEqual(attachment_filename(sentinel.instance, '.dat'), 'files/courses/dat')


class TestAttachment(TestCase):
    """
    Test `Attachment` model features.
    """
    def setUp(self):
        # Temporary storage
        self.tmp_dir = mkdtemp(prefix='fuuk_tests_')
        self.addCleanup(rmtree, self.tmp_dir)
        storage_patcher = patch.object(Attachment._meta.get_field('file'), 'storage', FileSystemStorage(self.tmp_dir))
        self.addCleanup(storage_patcher.stop)
        storage_patcher.start()

        self.course = Course.objects.create(code='COUR123')

    def test_file_simple(self):
        # Test file is stored correctly
        attachment = Attachment(course=self.course)
        attachment.file.save('foo.txt', ContentFile('content'))

        self.assertEqual(attachment.file.name, 'files/courses/foo.txt')
        self.assertEqual(attachment.file.size, 7)
        self.assertEqual(attachment.file.read(), b'content')
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, 'files/courses/foo.txt')))
        attachment.file.close()

    def test_file_unicode(self):
        # Test file with unicode name is stored correctly
        attachment = Attachment(course=self.course)
        attachment.file.save('šč řžě.txt', ContentFile('content'))

        self.assertEqual(attachment.file.name, 'files/courses/sc-rze.txt')
        self.assertEqual(attachment.file.size, 7)
        self.assertEqual(attachment.file.read(), b'content')
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, 'files/courses/sc-rze.txt')))
        attachment.file.close()
