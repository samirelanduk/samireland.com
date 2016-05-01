from django.core.files.uploadedfile import SimpleUploadedFile
from . import MediaTest
from media.forms import MediaForm
from media.models import MediaFile

class FormsRenderingTests(MediaTest):

    def test_media_form_has_correct_inputs(self):
        form = MediaForm()
        self.assertIn(
         'name="mediatitle" type="text"',
         str(form)
        )
        self.assertIn(
         'name="mediafile" type="file"',
         str(form)
        )



class FormsValidationTests(MediaTest):

    def test_media_form_wont_accept_blank_title(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        form = MediaForm(data={
         "mediatitle": "",
         "mediafile": media_file
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["mediatitle"],
         ["You cannot submit media with no title"]
        )


    def test_media_form_wont_accept_duplicate_titles(self):
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        MediaFile.objects.create(mediatitle="test", mediafile=media_file)
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        form = MediaForm(data={
         "mediatitle": "test",
         "mediafile": media_file
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["mediatitle"],
         ["There is already media with this title"]
        )
