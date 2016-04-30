from django.core.files.uploadedfile import SimpleUploadedFile
from . import MediaTest
from media.forms import MediaForm
from media.models import Image

class FormsRenderingTests(MediaTest):

    def test_media_form_has_correct_inputs(self):
        form = MediaForm()
        self.assertIn(
         'name="imagetitle" type="text"',
         str(form)
        )
        self.assertIn(
         'name="imagefile" type="file"',
         str(form)
        )



class FormsValidationTests(MediaTest):

    def test_media_form_wont_accept_blank_title(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        form = MediaForm(data={
         "imagetitle": "",
         "imagefile": image_file
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["imagetitle"],
         ["You cannot submit media with no title"]
        )


    def test_media_form_wont_accept_duplicate_titles(self):
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        Image.objects.create(imagetitle="test", imagefile=image_file)
        image_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        form = MediaForm(data={
         "imagetitle": "test",
         "imagefile": image_file
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["imagetitle"],
         ["There is already media with this title"]
        )
