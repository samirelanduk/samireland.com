"""Contains tests for the about section."""

from time import sleep
from .base import FunctionalTest

class AboutPageTests(FunctionalTest):

    def test_about_page_structure(self):
        self.browser.set_window_size(800, 600)
        self.get("/")

        # The last nav link goes to the about page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[-1].click()
        self.check_page("/about/")

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        about_bio = main.find_element_by_id("about-bio")

        # There is no edit link because they are not logged in
        links = about_bio.find_elements_by_tag_name("a")
        self.assertEqual(len(links),0)


    def test_can_change_about_page_text(self):
        self.check_can_edit_text("/about/", "about-bio", "about")


    def test_cannot_access_about_edit_page_when_not_logged_in(self):
        self.get("/edit/about/")
        self.check_page("/")
