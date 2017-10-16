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
        no_publications = publications.find_element_by_class_name("no-pub")


    def test_can_change_research_page_text(self):
        self.check_can_edit_text("/research/", "research-summary", "research")


    def test_cannot_access_research_edit_page_when_not_logged_in(self):
        self.get("/edit/research/")
        self.check_page("/")



class PublicationAdditionTests(FunctionalTest):

    def test_publication_addition(self):
        # User goes to research page
        self.get("/research/")

        # Publications div has no section for adding new pub
        publications = self.browser.find_element_by_id("publications")
        new = publications.find_elements_by_class_name("new-publication")
        self.assertEqual(len(new), 0)

        # They log in, and now there is
        self.login()
        self.get("/research/")
        publications = self.browser.find_element_by_id("publications")
        new = publications.find_element_by_class_name("new-publication")

        # They click it, and are taken to the new publication page
        link = new.find_element_by_tag_name("a")
        self.click(link)
        self.check_page("/research/new/")
        self.check_title("New Publication")
        self.check_h1("New Publication")


    def test_cannot_access_new_research_page_when_not_logged_in(self):
        self.get("/research/new/")
        self.check_page("/")
