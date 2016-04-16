from django.test import TestCase
from blog.views import home_page
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        resolved_view = resolve("/")
        self.assertEqual(resolved_view.func, home_page)


    def test_home_page_view_uses_home_page_template(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertEqual(response.content.decode(), expected_html)
