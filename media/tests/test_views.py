from django.test import TestCase
from media import views

class ViewTest(TestCase):
    pass


class MediaPageTests(ViewTest):

    def test_media_page_view_uses_media_page_template(self):
        response = self.client.get("/media/")
        self.assertTemplateUsed(response, "media_page.html")



class UploadMediaPageTests(ViewTest):

    def test_upload_media_page_view_uses_upload_media_template(self):
        response = self.client.get("/media/upload/")
        self.assertTemplateUsed(response, "upload_media.html")



class DeleteMediaPageTests(ViewTest):

    def test_delete_media_page_view_uses_delete_media_template(self):
        response = self.client.get("/media/delete/x/")
        self.assertTemplateUsed(response, "delete_media.html")
