from django.test import TestCase
from blog.views import home_page
from django.core.urlresolvers import resolve

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        resolved_view = resolve("/")
        self.assertEqual(resolved_view.func, home_page)
