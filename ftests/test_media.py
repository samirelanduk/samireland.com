from time import sleep
from .base import FunctionalTest

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


    def test_cannot_access_media_page_when_not_logged_in(self):
        self.get("/media/")
        self.check_page("/")
