from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from media.forms import MediaForm
from media.models import Image
from . import MediaTest
from media import views



class MediaPageTests(MediaTest):

    def test_media_page_view_uses_media_page_template(self):
        response = self.client.get("/media/")
        self.assertTemplateUsed(response, "media_page.html")


    def test_media_page_view_shows_images(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image1 = Image.objects.create(imagetitle="test", imagefile=image_file)
        image_file2 = SimpleUploadedFile("test2.png", b"\x00\x01\x02\x03")
        image2 = Image.objects.create(imagetitle="test2", imagefile=image_file2)

        response = self.client.get("/media/")
        try:
            self.assertContains(response, "test.png")
            self.assertContains(response, "test2.png")
        finally:
            image1.delete()
            image2.delete()



class UploadMediaPageTests(MediaTest):

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


    def test_upload_media_page_view_can_save_image(self):
        self.assertEqual(Image.objects.all().count(), 0)
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        self.client.post("/media/upload/", data={
         "imagetitle": "test",
         "imagefile": image_file
        })
        self.assertEqual(Image.objects.all().count(), 1)



class DeleteMediaPageTests(MediaTest):

    def test_delete_media_page_view_uses_delete_media_template(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image.objects.create(imagetitle="nameofthisfile", imagefile=image_file)
        try:
            response = self.client.get("/media/delete/nameofthisfile/")
            self.assertTemplateUsed(response, "delete_media.html")
        finally:
            image.delete()


    def test_delete_media_page_contains_image_title(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image.objects.create(imagetitle="nameofthisfile", imagefile=image_file)
        try:
            response = self.client.get("/media/delete/%s/" % image.imagetitle)
            self.assertContains(response, image.imagetitle)
        finally:
            image.delete()


    def test_delete_media_page_views_redirects_after_post(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image.objects.create(imagetitle="nameofthisfile", imagefile=image_file)
        try:
            response = self.client.post("/media/delete/%s/" % image.imagetitle)
            self.assertRedirects(response, "/media/")
        finally:
            image.delete()


    def test_delete_media_view_can_actually_delete_media(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image.objects.create(imagetitle="nameofthisfile", imagefile=image_file)
        try:
            self.assertEqual(Image.objects.count(), 1)
            self.client.post("/media/delete/%s/" % image.imagetitle)
            self.assertEqual(Image.objects.count(), 0)
        finally:
            image.delete()
