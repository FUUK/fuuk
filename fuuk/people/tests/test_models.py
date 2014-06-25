import unittest

from django.core.exceptions import ValidationError

from fuuk.people.models.article import doi_validator
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
