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

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        title_input = form.find_elements_by_tag_name("input")[0]
        date_input = form.find_elements_by_tag_name("input")[1]
        url_input = form.find_elements_by_tag_name("input")[2]
        doi_input = form.find_elements_by_tag_name("input")[3]
        authors_input = form.find_elements_by_tag_name("input")[4]
        abstract_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]

        # They submit a publication
        title_input.send_keys("The isolation of a novel dank meme")
        date_input.send_keys("28-09-1990")
        url_input.send_keys("http://journal-of-memology/12345/")
        doi_input.send_keys("10.1002/bip.23067")
        authors_input.send_keys("Marvin Goodwright, Tony **Blair**, Sam Ireland")
        abstract_input.send_keys("We report here the isolation of a new meme.")
        body_input.send_keys("Line 1\n\nLine2\n\nLine 3")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.click(submit_button)

        # They are on the page for that publication
        self.check_page("/research/the-isolation-of-a-novel-dank-meme/")


    def test_cannot_access_new_research_page_when_not_logged_in(self):
        self.get("/research/new/")
        self.check_page("/")
