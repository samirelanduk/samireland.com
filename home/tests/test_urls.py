from samireland.tests import UrlTest
from home import views

class HomeUrlTests(UrlTest):

    def test_home_page_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/", views.home_page)


    def test_login_url_resolves_to_login_view(self):
        self.check_url_returns_view("/authenticate/", views.login_page)
