from time import sleep
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from .base import FunctionalTest
from samireland.settings import BASE_DIR, MEDIA_ROOT
from media.models import MediaFile

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

        # They click it and are taken to the piano update page
        media_link.click()
        self.check_page("/media/")

        # There is a header, and a div for the media grid
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertIn("media", h1.text.lower())
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


    def test_cannot_upload_media_with_no_file(self):
        self.login()
        self.get("/media/")

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")

        # There is a file input and a name input
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload no image and call it 'test image'
        name_input.send_keys("test-image")

        # They click the submit button
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # They are still on the same page
        self.check_page("/media/")

        # The grid is still empty
        grid = self.browser.find_element_by_id("media-grid")
        self.assertEqual(len(grid.find_elements_by_class_name("media-square")), 0)

        # The form has an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "You must supply a file.")


    def test_cannot_upload_media_with_no_title(self):
        self.login()
        self.get("/media/")

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")

        # There is a file input and a name input
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload am image but no title
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")

        # They click the submit button
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # They are still on the same page
        self.check_page("/media/")

        # The grid is still empty
        grid = self.browser.find_element_by_id("media-grid")
        self.assertEqual(len(grid.find_elements_by_class_name("media-square")), 0)

        # The form has an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "You must supply a title.")


    def test_cannot_upload_media_with_duplicate_title(self):
        self.login()
        self.get("/media/")

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")

        # There is a file input and a name input
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload an image correctly
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")
        name_input.send_keys("test-image")

        # They click the submit button
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # They are still on the same page
        self.check_page("/media/")

        # There is a form for uploading media
        form = self.browser.find_element_by_tag_name("form")

        # There is a file input and a name input
        file_input, name_input = form.find_elements_by_tag_name("input")[:2]
        self.assertEqual(file_input.get_attribute("type"), "file")
        self.assertEqual(name_input.get_attribute("type"), "text")

        # They upload an image correctly but with the same title
        file_input.send_keys(BASE_DIR + "/samireland/static/images/favicon-96x96.png")
        name_input.send_keys("test-image")

        # They click the submit button
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # The grid still only has one element
        grid = self.browser.find_element_by_id("media-grid")
        self.assertEqual(len(grid.find_elements_by_class_name("media-square")), 1)

        # The form has an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "There is already a file with title.")



class MediaDeletionTests(MediaTest):

    def test_can_delete_media(self):
        # Add three images
        MediaFile.objects.create(
         mediatitle="file1", mediafile=SimpleUploadedFile("test.png", b"\x00\x01")
        )
        MediaFile.objects.create(
         mediatitle="file2", mediafile=SimpleUploadedFile("test.png", b"\x00\x01")
        )

        # They go to the media page
        self.login()
        self.get("/media/")

        # There is a header, and a div for the media grid
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertIn("media", h1.text.lower())
        grid = self.browser.find_element_by_id("media-grid")

        # The grid has two images
        media = grid.find_elements_by_class_name("media-square")
        self.assertEqual(len(media), 2)
        self.assertIn("file1", media[0].find_element_by_class_name("image_title").text)
        self.assertIn("file2", media[1].find_element_by_class_name("image_title").text)

        # Each image has a delete button
        button1 = media[0].find_element_by_tag_name("a")
        button2 = media[1].find_element_by_tag_name("a")
        self.assertEqual(button1.text, "Delete")
        self.assertEqual(button2.text, "Delete")

        # They click the first delete button
        button1.click()

        # They are now on the media delete page
        self.assertRegex(
         self.browser.current_url, self.live_server_url + "/media/delete/(.+)/"
        )

        # There is a deletion form
        form = self.browser.find_element_by_tag_name("form")
        description = form.find_element_by_id("delete-description")
        self.assertIn("file1", description.text)
        warning = form.find_element_by_id("delete-warning")
        self.assertIn(
         "are you sure?",
         warning.text.lower()
        )
        image = form.find_element_by_tag_name("img")

        # There is a back to safety link, and a delete button
        back_to_safety = form.find_element_by_tag_name("a")
        delete_button = form.find_elements_by_tag_name("input")[-1]

        # He goes back to safety
        back_to_safety.click()
        self.check_page("/media/")
        grid = self.browser.find_element_by_id("media-grid")
        media = grid.find_elements_by_class_name("media-square")
        button1 = media[0].find_element_by_tag_name("a")
        button2 = media[1].find_element_by_tag_name("a")

        # He changes his mind and goes back
        button1.click()
        self.assertRegex(
         self.browser.current_url, self.live_server_url + "/media/delete/(.+)/"
        )
        form = self.browser.find_element_by_tag_name("form")
        delete_button = form.find_elements_by_tag_name("input")[-1]


        # He deletes, and is taken back to the edit page
        delete_button.click()
        self.check_page("/media/")

        # The file has gone
        grid = self.browser.find_element_by_id("media-grid")
        media = grid.find_elements_by_class_name("media-square")
        self.assertEqual(len(media), 1)
        self.assertIn("file2", media[0].find_element_by_class_name("image_title").text)



class MediaAccessTests(MediaTest):

    def test_cannot_access_media_page_when_not_logged_in(self):
        self.get("/media/")
        self.check_page("/")


    def test_cannot_access_media_delete_page_when_not_logged_in(self):
        self.get("/media/delete/file.png/")
        self.check_page("/")
