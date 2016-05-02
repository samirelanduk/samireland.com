from django.test import TestCase
from django.core.urlresolvers import resolve
from account import views

class TestUrls(TestCase):

    def test_login_url_resolves_to_login_view(self):
        resolver = resolve("/account/login/")
        self.assertEqual(resolver.func, views.login_page)
