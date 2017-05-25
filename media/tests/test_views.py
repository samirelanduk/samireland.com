import os
from django.core.files.uploadedfile import SimpleUploadedFile
from samireland.settings import MEDIA_ROOT
from media.models import MediaFile
from samireland.tests import ViewTest

class MediaPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.client.login(username="testsam", password="testpassword")
        self.media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass


    def test_media_view_uses_media_template(self):
        response = self.client.get("/media/")
        self.assertTemplateUsed(response, "media.html")


    def test_cannot_access_media_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/media/")
        self.assertRedirects(response, "/")


    def test_media_view_redirects_on_post(self):
        response = self.client.post(
         "/media/", data={"file": self.media_file, "title":"Test"}
        )
        self.assertRedirects(response, "/media/")


    def test_media_view_saves_file(self):
        response = self.client.post(
         "/media/", data={"file": self.media_file, "title":"Test"}
        )
        self.assertEqual(MediaFile.objects.all().count(), 1)
        self.assertEqual(MediaFile.objects.first().mediatitle, "Test")


    def test_media_view_handles_missing_file(self):
        response = self.client.post(
         "/media/", data={"file": None, "title":"Test"}
        )
        self.assertEqual(MediaFile.objects.count(), 0)
        self.assertIn("media", response.context)
        self.assertEqual(
         response.context["error_text"],
         "You must supply a file."
        )


    def test_media_view_handles_missing_title(self):
        response = self.client.post(
         "/media/", data={"file": self.media_file, "title":""}
        )
        self.assertEqual(MediaFile.objects.count(), 0)
        self.assertIn("media", response.context)
        self.assertEqual(
         response.context["error_text"],
         "You must supply a title."
        )


    def test_media_view_handles_duplicate_title(self):
        self.client.post(
         "/media/", data={"file": self.media_file, "title":"title"}
        )
        self.assertEqual(MediaFile.objects.count(), 1)
        response = self.client.post(
         "/media/", data={"file": self.media_file, "title":"title"}
        )
        self.assertEqual(MediaFile.objects.count(), 1)
        self.assertIn("media", response.context)
        self.assertEqual(
         response.context["error_text"],
         "There is already a file with title."
        )


    def test_media_view_sends_media(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image2 = MediaFile(mediatitle="test2", mediafile=self.media_file)
        image1.save()
        image2.save()
        response = self.client.get("/media/")
        self.assertEqual(response.context["media"][0], image1)
        self.assertEqual(response.context["media"][1], image2)




class MediaPageDeleteViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.client.login(username="testsam", password="testpassword")
        self.media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass


    def test_media_delete_view_uses_media_template(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image1.save()
        response = self.client.get("/media/delete/test1/")
        self.assertTemplateUsed(response, "media-delete.html")


    def test_cannot_access_media_delete_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/media/delete/file.png/")
        self.assertRedirects(response, "/")


    def test_media_view_sends_media(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image2 = MediaFile(mediatitle="test2", mediafile=self.media_file)
        image1.save()
        image2.save()
        response = self.client.get("/media/delete/{}/".format("test2"))
        self.assertEqual(response.context["media"], image2)


    def test_media_delete_view_handles_incorrect_title(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image2 = MediaFile(mediatitle="test2", mediafile=self.media_file)
        image1.save()
        image2.save()
        response = self.client.get("/media/delete/{}/".format("test3"))
        self.assertRedirects(response, "/media/")


    def test_media_view_redirects_on_post(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image1.save()
        response = self.client.post("/media/delete/test1/")
        self.assertRedirects(response, "/media/")


    def test_media_delete_view_cam_delete_views(self):
        image1 = MediaFile(mediatitle="test1", mediafile=self.media_file)
        image2 = MediaFile(mediatitle="test2", mediafile=self.media_file)
        image1.save()
        image2.save()
        self.client.post("/media/delete/test1/")
        self.assertEqual(MediaFile.objects.count(), 1)
        self.assertEqual(MediaFile.objects.first(), image2)
        self.client.post("/media/delete/test2/")
        self.assertEqual(MediaFile.objects.count(), 0)
