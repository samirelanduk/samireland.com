from .base import FunctionalTest

class MediaUploadPageTests(FunctionalTest):

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
