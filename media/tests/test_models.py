import os
import time
from datetime import datetime
from unittest.mock import Mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from media.models import MediaFile, create_filename
from samireland.tests import ModelTest
from samireland.settings import MEDIA_ROOT

class MediaTest(ModelTest):

    def setUp(self):
        ModelTest.setUp(self)
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass



class FileNameCreationTests(MediaTest):

    def test_can_get_filename_extension(self):
        instance = Mock()
        name = create_filename(instance, "filename.bmp")
        self.assertEqual(name[-4:], ".bmp")


    def test_can_get_filename_name_is_timestamp(self):
        instance = Mock()
        now = datetime.now()
        name = create_filename(instance, "filename.bmp")
        datetime.strptime(name[:-4], "%Y%m%d%H%M%S")



class ModelCreationTest(MediaTest):

    def test_can_save_images(self):
        self.assertNotIn("test.png", os.listdir(MEDIA_ROOT))
        self.assertEqual(MediaFile.objects.all().count(), 0)

        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(mediatitle="test", mediafile=media_file)
        image.save()

        self.assertEqual(MediaFile.objects.all().count(), 1)
        self.assertIn(
         datetime.now().strftime("%Y%m%d%H%M%S") + ".png",
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
         datetime.now().strftime("%Y%m%d%H%M%S") + ".png",
         os.listdir(MEDIA_ROOT)
        )

        image.delete()
        self.assertEqual(MediaFile.objects.all().count(), 0)
        time.sleep(1)
        self.assertNotIn(
         datetime.now().strftime("%Y%m%d%H%M%S") + ".png",
         os.listdir(MEDIA_ROOT)
        )



class ModelValidationTests(MediaTest):

    def test_cannot_save_image_with_no_title(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
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
