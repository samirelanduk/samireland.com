from samireland.tests import UrlTest
from piano import views

class PianoUrlTests(UrlTest):

    def test_piano_page_url_resolves_to_piano_page_view(self):
        self.check_url_returns_view("/piano/", views.piano_page)


    def test_piano_update_page_url_resolves_to_piano_update_page_view(self):
        self.check_url_returns_view("/piano/update/", views.piano_update_page)


    def test_piano_delete_page_url_resolves_to_piano_delete_page_view(self):
        self.check_url_returns_view("/piano/delete/1/", views.piano_delete_page)
        self.check_url_returns_view("/piano/delete/9/", views.piano_delete_page)
