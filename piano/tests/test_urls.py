from django.core.urlresolvers import resolve
from django.test import TestCase
from piano import views

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)


    def test_root_piano_url_resolves_to_piano_home_page_view(self):
        self.check_url_returns_view("/piano/", views.piano_page)


    def test_practice_url_resolves_to_practice_page_view(self):
        self.check_url_returns_view("/piano/practice/", views.practice_page)


    def test_update_url_resolves_to_update_page_view(self):
        self.check_url_returns_view("/piano/update/", views.update_page)
