from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from media.forms import MediaForm
from media.models import MediaFile
from . import MediaTest
from media import views



class MediaPageTests(MediaTest):

    def test_media_page_view_is_protected(self):
        response = self.client.get("/media/")
        self.assertRedirects(response, "/")


    def test_media_page_view_uses_media_page_template(self):
        response = self.client.get("/media/")
        self.assertTemplateUsed(response, "media_page.html")


    def test_media_page_view_shows_images(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        media1 = MediaFile.objects.create(mediatitle="test", mediafile=media_file)
        media_file2 = SimpleUploadedFile("test2.png", b"\x00\x01\x02\x03")
        media2 = MediaFile.objects.create(mediatitle="test2", mediafile=media_file2)

        response = self.client.get("/media/")
        try:
            self.assertContains(response, media1.mediafile.url)
            self.assertContains(response, media2.mediafile.url)
        finally:
            media1.delete()
            media2.delete()



class UploadMediaPageTests(MediaTest):

    def test_upload_media_page_view_is_protected(self):
        response = self.client.get("/media/upload/")
        self.assertRedirects(response, "/")

    def test_upload_media_page_view_uses_upload_media_template(self):
        response = self.client.get("/media/upload/")
        self.assertTemplateUsed(response, "upload_media.html")


    def test_upload_media_page_view_uses_upload_media_form(self):
        response = self.client.get("/media/upload/")
        self.assertIsInstance(response.context["form"], MediaForm)


    def test_upload_media_page_view_redirects_after_post(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        response = self.client.post("/media/upload/", data={
         "mediatitle": "test",
         "mediafile": media_file
        })
        self.assertRedirects(response, "/media/")


    def test_upload_media_page_view_can_save_image(self):
        self.assertEqual(MediaFile.objects.all().count(), 0)
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        self.client.post("/media/upload/", data={
         "mediatitle": "test",
         "mediafile": media_file
        })
        self.assertEqual(MediaFile.objects.all().count(), 1)



class DeleteMediaPageTests(MediaTest):

    def test_delete_media_page_view_is_protected(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile.objects.create(mediatitle="nameofthisfile", mediafile=media_file)
        try:
            response = self.client.get("/media/delete/nameofthisfile/")
            self.assertRedirects(response, "/")
        finally:
            image.delete()


    def test_delete_media_page_view_uses_delete_media_template(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile.objects.create(mediatitle="nameofthisfile", mediafile=media_file)
        try:
            response = self.client.get("/media/delete/nameofthisfile/")
            self.assertTemplateUsed(response, "delete_media.html")
        finally:
            image.delete()


    def test_delete_media_page_contains_image_title(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile.objects.create(mediatitle="nameofthisfile", mediafile=media_file)
        try:
            response = self.client.get("/media/delete/%s/" % image.mediatitle)
            self.assertContains(response, image.mediatitle)
        finally:
            image.delete()


    def test_delete_media_page_views_redirects_after_post(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile.objects.create(mediatitle="nameofthisfile", mediafile=media_file)
        try:
            response = self.client.post("/media/delete/%s/" % image.mediatitle)
            self.assertRedirects(response, "/media/")
        finally:
            image.delete()


    def test_delete_media_view_can_actually_delete_media(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile.objects.create(mediatitle="nameofthisfile", mediafile=media_file)
        try:
            self.assertEqual(MediaFile.objects.count(), 1)
            self.client.post("/media/delete/%s/" % image.mediatitle)
            self.assertEqual(MediaFile.objects.count(), 0)
        finally:
            image.delete()
