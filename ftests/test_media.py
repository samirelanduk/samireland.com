import os
from django.core.files.uploadedfile import SimpleUploadedFile
from .base import FunctionalTest
from samireland.models import MediaFile
from samireland.settings import BASE_DIR, MEDIA_ROOT

class MediaTest(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass
        FunctionalTest.tearDown(self)



class MediaUploadTests(MediaTest):

    def test_can_upload_images(self):
        self.login()
        self.get("/")

        # There is a media link in the header
        header = self.browser.find_element_by_tag_name("header")
        media_link = header.find_element_by_id("media-link")

        # They click it and are taken to the media page
        media_link.click()
        self.check_page("/media/")

        # There is a header, and a div for the media grid
        self.check_title("Media")
        self.check_h1("Media")
        grid = self.browser.find_element_by_id("media-grid")

        # The grid is empty
        self.assertEqual(len(grid.find_elements_by_class_name("media-square")), 0)

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")

        # There is a file input and a name input
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload an image and call it 'test image'
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")
        name_input.send_keys("test-image")

        # They click the submit button
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # They are still on the same page
        self.check_page("/media/")

        # The grid now has one item
        grid = self.browser.find_element_by_id("media-grid")
        media = grid.find_elements_by_class_name("media-square")
        self.assertEqual(len(media), 1)

        # The media's text is the title
        self.assertIn("test-image", media[0].text)

        # It has the image as background
        self.assertTrue(media[0].value_of_css_property("background-image").endswith(".png\")"))


    def test_cannot_upload_media_with_duplicate_title(self):
        self.login()
        self.get("/media/")

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload an image correctly
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")
        name_input.send_keys("test-image")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.click(submit_button)

        # They are still on the same page
        self.check_page("/media/")

        # They upload an image with duplicate name
        form = self.browser.find_element_by_tag_name("form")
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")
        name_input.send_keys("test-image")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.click(submit_button)

        # The grid still only has one element
        grid = self.browser.find_element_by_id("media-grid")
        self.assertEqual(len(grid.find_elements_by_class_name("media-square")), 1)

        # The form has an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error-message")
        self.assertEqual(error.text, "There is already media with that name")



class MediaDeletionTests(MediaTest):

    def test_can_delete_media(self):
        # Add three images
        MediaFile.objects.create(
         name="file1", mediafile=SimpleUploadedFile("test1.png", b"\x00\x01")
        )
        MediaFile.objects.create(
         name="file2", mediafile=SimpleUploadedFile("test2.png", b"\x01\x02")
        )

        # They go to the media page
        self.login()
        self.get("/media/")

        # The grid has two images
        grid = self.browser.find_element_by_id("media-grid")
        media = grid.find_elements_by_class_name("media-square")
        self.assertEqual(len(media), 2)
        self.assertIn("file1", media[0].find_element_by_class_name("image_title").text)
        self.assertIn("file2", media[1].find_element_by_class_name("image_title").text)

        # Each image has a delete button
        button1 = media[0].find_element_by_tag_name("button")
        button2 = media[1].find_element_by_tag_name("button")
        self.assertEqual(button1.text, "Delete")
        self.assertEqual(button2.text, "Delete")

        # There is a hidden form in the first one
        form = media[0].find_element_by_tag_name("form")
        self.check_invisible(form)

        # They click delete and the form appears
        self.click(button1)
        self.check_visible(form)

        # The form asks them if they really want to delete and they back down
        self.assertIn("sure", form.text)
        no = form.find_element_by_tag_name("button")
        self.assertIn("No", no.text)
        self.click(no)
        self.check_invisible(form)

        # They change their mind and delete
        self.click(button1)
        self.check_visible(form)
        yes = form.find_elements_by_tag_name("input")[-1]
        self.assertIn("Yes", yes.get_attribute("value"))
        self.click(yes)

        # They are still on the same page and the image is gone
        self.check_page("/media/")
        grid = self.browser.find_element_by_id("media-grid")
        media = grid.find_elements_by_class_name("media-square")
        self.assertEqual(len(media), 1)
        self.assertIn("file2", media[0].find_element_by_class_name("image_title").text)
