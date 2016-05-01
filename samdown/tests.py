import datetime
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from media.models import Image
import samdown

class PostSplittingTests(TestCase):

    def test_one_block_returns_one_block(self):
        self.assertEqual(
         samdown.split("This is a paragraph"),
         ["This is a paragraph"]
        )


    def test_single_new_line_does_not_split(self):
        self.assertEqual(
         samdown.split("This is a paragraph\nThis is the same paragraph"),
         ["This is a paragraph\nThis is the same paragraph"]
        )


    def test_can_split(self):
        self.assertEqual(
         samdown.split("This is a paragraph\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )


    def test_multi_new_lines_ignored(self):
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a   paragraph\n\n\nThis is a new paragraph\n\n\nAnd a third"),
         ["This is a   paragraph", "This is a new paragraph", "And a third"]
        )


    def test_windows_new_lines_work(self):
        self.assertEqual(
         samdown.split("This is a paragraph\r\n\r\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )



class BlockFormattingTests(TestCase):

    def test_plain_block_returns_plain_p(self):
        self.assertEqual(
         samdown.process_block("A paragraph"),
         "<p>A paragraph</p>"
        )


    def test_italics_processing(self):
        self.assertEqual(
         samdown.process_block("*Some* italics text"),
         "<p><em>Some</em> italics text</p>"
        )
        self.assertEqual(
         samdown.process_block("*Some* *italics* text"),
         "<p><em>Some</em> <em>italics</em> text</p>"
        )
        self.assertEqual(
         samdown.process_block("Some italics *text*"),
         "<p>Some italics <em>text</em></p>"
        )


    def test_bold_processing(self):
        self.assertEqual(
         samdown.process_block("**Some** bold text"),
         "<p><b>Some</b> bold text</p>"
        )
        self.assertEqual(
         samdown.process_block("**Some** **bold** text"),
         "<p><b>Some</b> <b>bold</b> text</p>"
        )
        self.assertEqual(
         samdown.process_block("Some bold **text**"),
         "<p>Some bold <b>text</b></p>"
        )


    def test_underline_processing(self):
        self.assertEqual(
         samdown.process_block("_Some_ underlined text"),
         "<p><u>Some</u> underlined text</p>"
        )
        self.assertEqual(
         samdown.process_block("_Some_ _underlined_ text"),
         "<p><u>Some</u> <u>underlined</u> text</p>"
        )
        self.assertEqual(
         samdown.process_block("Some underlined _text_"),
         "<p>Some underlined <u>text</u></p>"
        )


    def test_mixed_formatting(self):
        self.assertEqual(
         samdown.process_block("_Some_ *formatted* **text***"),
         "<p><u>Some</u> <em>formatted</em> <b>text</b>*</p>"
        )



class BlockHyperlinkTests(TestCase):

    def test_can_process_hyperlink(self):
        self.assertEqual(
         samdown.process_hyperlink("[link](http://test.com/)"),
         "<a href=\"http://test.com/\">link</a>"
        )


    def test_can_process_hyperlink_on_new_page(self):
        self.assertEqual(
         samdown.process_hyperlink("[link](http://test.com/ newpage)"),
         "<a href=\"http://test.com/\" target=\"_blank\">link</a>"
        )


    def test_hyperlink_translation(self):
        self.assertEqual(
         samdown.process_block("A [link](http://test.com)."),
         "<p>A <a href=\"http://test.com\">link</a>.</p>"
        )


    def test_multiple_hyperlink_translation(self):
        self.assertEqual(
         samdown.process_block("A [link](http://test.com)[.](/about/)"),
         "<p>A <a href=\"http://test.com\">link</a><a href=\"/about/\">.</a></p>"
        )



class BlockTypeTests(TestCase):

    def test_normal_block_produces_paragraph(self):
        self.assertTrue(samdown.process_block("...").startswith("<p>"))
        self.assertTrue(samdown.process_block("[YOUTUBE](xxxx).").startswith("<p>"))
        self.assertTrue(samdown.process_block(".[YOUTUBE](xxxx)").startswith("<p>"))


    def test_youtube_block_produces_iframe(self):
        self.assertTrue(samdown.process_block("[YOUTUBE](xxxxx)").startswith(
         "<div class=\"youtube\"><iframe"))


    def test_img_block_produces_image(self):
        image_file = SimpleUploadedFile("downtest.png", b"\x00\x01\x02\x03")
        image = Image.objects.create(imagetitle="test", imagefile=image_file)
        try:
            self.assertTrue(samdown.process_block("[IMAGE](test)").startswith(
             "<figure><img"))
            self.assertIn("%s.png" % datetime.datetime.now().strftime("%Y%m%d"), samdown.process_block("[IMAGE](test)"))
        finally:
            image.delete()


    def test_img_alt_text(self):
        self.assertIn(
         'title="ALT TEXT"',
         samdown.process_block('[IMAGE](xxxxx A:"ALT TEXT")')
        )


    def test_img_caption_text(self):
        self.assertIn(
         '<figcaption>A CAPTION</figcaption>',
         samdown.process_block('[IMAGE](xxxxx C:"A CAPTION")')
        )


    def test_img_alt_text_and_caption(self):
        self.assertIn(
         'title="ALT TEXT"',
         samdown.process_block('[IMAGE](xxxxx A:"ALT TEXT" C:"A CAPTION")')
        )
        self.assertIn(
         '<figcaption>A CAPTION</figcaption>',
         samdown.process_block('[IMAGE](xxxxx A:"ALT TEXT" C:"A CAPTION")')
        )
        self.assertIn(
         'title="ALT TEXT"',
         samdown.process_block('[IMAGE](xxxxx C:"A CAPTION" A:"ALT TEXT")')
        )
        self.assertIn(
         '<figcaption>A CAPTION</figcaption>',
         samdown.process_block('[IMAGE](xxxxx C:"A CAPTION" A:"ALT TEXT")')
        )


    def test_video_block_produces_block(self):
        video_file = SimpleUploadedFile("downtest.mov", b"\x00\x01\x02\x03")
        video = Image.objects.create(imagetitle="test", imagefile=video_file)
        try:
            self.assertTrue(samdown.process_block("[VIDEO](test)").startswith(
             "<video src="))
            self.assertIn("%s.mov" % datetime.datetime.now().strftime("%Y%m%d"), samdown.process_block("[VIDEO](test)"))
        finally:
            video.delete()
