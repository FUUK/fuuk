import unittest

from django.core.exceptions import ValidationError

from fuuk.people.models.article import doi_validator


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
