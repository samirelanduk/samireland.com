from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from media.forms import MediaForm
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


    def test_upload_media_page_view_uses_upload_media_form(self):
        response = self.client.get("/media/upload/")
        self.assertIsInstance(response.context["form"], MediaForm)


    def test_upload_media_page_view_redirects_after_post(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        response = self.client.post("/media/upload/", data={
         "imagetitle": "test",
         "imagefile": image_file
        })
        self.assertRedirects(response, "/media/")



class DeleteMediaPageTests(ViewTest):

    def test_delete_media_page_view_uses_delete_media_template(self):
        response = self.client.get("/media/delete/x/")
        self.assertTemplateUsed(response, "delete_media.html")
