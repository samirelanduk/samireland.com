from django.core.urlresolvers import resolve, Resolver404
from django.test import TestCase
from media import views

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)


    def test_media_url_resolves_to_media_page_view(self):
        self.check_url_returns_view("/media/", views.media_page)


    def test_upload_url_resolves_to_upload_page_view(self):
        self.check_url_returns_view("/media/upload/", views.upload_media_page)


    def test_delete_url_resolves_to_delete_page_view(self):
        self.check_url_returns_view("/media/delete/xxx.xxx/", views.delete_media_page)


    def test_media_urls_are_not_greedy(self):
        with self.assertRaises(Resolver404):
            resolve("/media/xxxx")
