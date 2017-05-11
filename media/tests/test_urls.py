from samireland.tests import UrlTest
from media import views

class MediaUrlTests(UrlTest):

    def test_piano_page_url_resolves_to_piano_page_view(self):
        self.check_url_returns_view("/media/", views.media_page)
