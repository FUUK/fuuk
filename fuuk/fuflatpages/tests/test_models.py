# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import clear_script_prefix, set_script_prefix
from django.test import TestCase

from fuuk.fuflatpages.models import FlatPage


class FlatpageModelTests(TestCase):

    def test_get_absolute_url_urlencodes(self):
        pf = FlatPage(title="Café!", url='/café/')
        self.assertEqual(pf.get_absolute_url(), '/caf%C3%A9/')

    def test_get_absolute_url_honors_script_prefix(self):
        pf = FlatPage(title="Tea!", url='/tea/')
        set_script_prefix('/beverages/')
        try:
            self.assertEqual(pf.get_absolute_url(), '/beverages/tea/')
        finally:
            clear_script_prefix()
