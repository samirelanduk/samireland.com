from samireland.tests import UrlTest
from blog import views

class BlogUrlTests(UrlTest):

    def test_new_blog_url_resolves_to_new_blog_view(self):
        self.check_url_returns_view("/blog/new/", views.new_blog_page)


    def test_blog_url_resolves_to_blog_view(self):
        self.check_url_returns_view("/blog/", views.blog_page)


    def test_blog_post_url_resolves_to_blog_view(self):
        self.check_url_returns_view("/blog/2000/9/28/", views.one_post_page)
