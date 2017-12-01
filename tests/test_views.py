from unittest.mock import patch, Mock
from seleniumx import TestCaseX
from django.http import Http404
from django.test import TestCase
from samireland.views import *

class HomeViewTests(TestCase, TestCaseX):

    def test_home_view_uses_home_template(self):
        request = self.get_request("/")
        self.check_view_uses_template(home, request, "home.html")
