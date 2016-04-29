from django.core.urlresolvers import resolve
from django.test import TestCase
from blog import views

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)


    def test_root_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/", views.home_page)


    def test_about_url_resolves_to_about_page_view(self):
        self.check_url_returns_view("/about/", views.about_page)


    def test_blog_url_resolves_to_blog_page_view(self):
        self.check_url_returns_view("/blog/", views.blog_page)


    def test_new_blog_post_url_resolves_to_new_blog_post_page_view(self):
        self.check_url_returns_view("/blog/new/", views.new_post_page)


    def test_edit_blog_posts_url_resolves_to_edit_blog_posts_page_view(self):
        self.check_url_returns_view("/blog/edit/", views.edit_posts_page)


    def test_edit_blog_post_url_resolves_to_edit_blog_post_page_view(self):
        self.check_url_returns_view("/blog/edit/23/", views.edit_post_page)


    def test_delete_blog_post_url_resolves_to_delete_blog_post_page_view(self):
        self.check_url_returns_view("/blog/delete/23/", views.delete_post_page)
