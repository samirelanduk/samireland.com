import os
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from media.models import Image
from samireland.settings import MEDIA_ROOT
from . import MediaTest

class ModelCreationTest(MediaTest):

    def test_can_save_images(self):
        self.assertNotIn("test.png", os.listdir(MEDIA_ROOT))
        self.assertEqual(Image.objects.all().count(), 0)

        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image(imagetitle="test", imagefile=image_file)
        image.save()

        self.assertEqual(Image.objects.all().count(), 1)
        self.assertIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )

        retrieved_image = Image.objects.first()
        self.assertEqual(retrieved_image, image)


    def test_can_delete_images(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image(imagetitle="test", imagefile=image_file)
        image.save()
        self.assertEqual(Image.objects.all().count(), 1)
        self.assertIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )

        image.delete()
        self.assertEqual(Image.objects.all().count(), 0)
        self.assertNotIn(
         datetime.datetime.now().strftime("%Y%m%d") + ".png",
         os.listdir(MEDIA_ROOT)
        )



class ModelValidationTest(MediaTest):

    def test_cannot_save_image_with_no_name(self):
        image_file = SimpleUploadedFile("", b"\x00\x01\x02\x03")
        image = Image(imagetitle="", imagefile=image_file)
        with self.assertRaises(ValidationError):
            image.full_clean()


    def test_cannot_have_images_with_duplicate_titles(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image(imagetitle="name", imagefile=image_file)
        image.save()
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = Image(imagetitle="name", imagefile=image_file)
        with self.assertRaises(ValidationError):
            image.full_clean()
