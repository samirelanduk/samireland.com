from samireland.tests import UrlTest
from media import views

class MediaUrlTests(UrlTest):

    def test_media_page_url_resolves_to_media_page_view(self):
        self.check_url_returns_view("/media/", views.media_page)


    def test_media_delete_page_url_resolves_to_media_delete_page_view(self):
        self.check_url_returns_view("/media/delete/file.png/", views.media_delete_page)
