from time import sleep
from .base import FunctionalTest
from samireland.settings import BASE_DIR

class MediaTest(FunctionalTest):
    pass



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
        self.assertEqual(media[0].text, "test-image")

        # It has the image as background
        self.assertTrue(media[0].value_of_css_property("background-url").endswith(".png"))




class MediaAccessTests(MediaTest):

    def test_cannot_access_media_page_when_not_logged_in(self):
        self.get("/media/")
        self.check_page("/")
