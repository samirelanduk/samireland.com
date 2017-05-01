"""Contains tests for the research section."""

from time import sleep
from .base import FunctionalTest

class ResearchPageTests(FunctionalTest):

    def test_research_page_structure(self):
        self.browser.set_window_size(800, 600)
        self.get("/")

        # The second nav link goes to the research page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[1].click()
        self.check_page("/research/")

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        research_summary = main.find_element_by_id("research-summary")

        # There is no edit link because they are not logged in
        links = research_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links),0)

        # There is a div for publications
        publications = main.find_element_by_id("publications")
        h2 = publications.find_elements_by_tag_name("h2")
        no_publications = publications.find_element_by_tag_name("p")


    def test_can_change_research_page_text(self):
        self.check_can_edit_text("/research/", "research-summary", "research")


    def test_cannot_access_research_edit_page_when_not_logged_in(self):
        self.get("/edit/research/")
        self.check_page("/")
