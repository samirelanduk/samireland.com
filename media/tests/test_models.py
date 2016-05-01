import os
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from media.models import MediaFile
from samireland.settings import MEDIA_ROOT
from . import MediaTest

class ModelCreationTest(MediaTest):

    def test_can_save_images(self):
        self.assertNotIn("test.png", os.listdir(MEDIA_ROOT))
        self.assertEqual(MediaFile.objects.all().count(), 0)

        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="test", mediafile=media_file)
        image.save()

        self.assertEqual(MediaFile.objects.all().count(), 1)
        self.assertIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )

        retrieved_image = MediaFile.objects.first()
        self.assertEqual(retrieved_image, image)


    def test_can_delete_images(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="test", mediafile=media_file)
        image.save()
        self.assertEqual(MediaFile.objects.all().count(), 1)
        self.assertIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )

        image.delete()
        self.assertEqual(MediaFile.objects.all().count(), 0)
        self.assertNotIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )



class ModelValidationTest(MediaTest):

    def test_cannot_save_image_with_no_name(self):
        media_file = SimpleUploadedFile("", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="", mediafile=media_file)
        with self.assertRaises(ValidationError):
            image.full_clean()


    def test_cannot_have_images_with_duplicate_titles(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="name", mediafile=media_file)
        image.save()
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="name", mediafile=media_file)
        with self.assertRaises(ValidationError):
            image.full_clean()
