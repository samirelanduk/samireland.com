"""Contains tests for the research section."""

from time import sleep
from .base import FunctionalTest

class ResearchTest(FunctionalTest):

    def enter_publication(self, id_, title, date, url, doi, authors, abstract, body):
        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        abstract_input = form.find_elements_by_tag_name("textarea")[0]
        body_input = form.find_elements_by_tag_name("textarea")[1]

        # They submit a publication
        id_input.send_keys(id_)
        title_input.send_keys(title)
        if date: date_input.send_keys(date)
        url_input.send_keys(url)
        doi_input.send_keys(doi)
        authors_input.send_keys(authors)
        abstract_input.send_keys(abstract)
        body_input.send_keys(body)
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.click(submit_button)


    def check_publication(self, date, external, authors, paragraphs):
        date_div = self.browser.find_element_by_id("date")
        external_div = self.browser.find_element_by_id("external-link")
        authors_div = self.browser.find_element_by_id("authors")
        body_div = self.browser.find_element_by_id("pub-body")

        self.assertEqual(date_div.text, date)
        self.assertEqual(external_div.text, external)
        self.assertEqual(authors_div.text, authors)
        paragraph_divs = body_div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraph_divs), len(paragraphs))
        for paragraph_div, paragraph_div_text in zip(paragraph_divs, paragraphs):
            self.assertEqual(paragraph_div.text, paragraph_div_text)



class ResearchPageTests(ResearchTest):

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



class PublicationAdditionTests(ResearchTest):

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

        # They enter a publication
        self.enter_publication(
         "novel-dank-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are on the page for that publication
        self.check_page("/research/novel-dank-meme/")
        self.check_title("The isolation of a novel dank meme")
        self.check_h1("The isolation of a novel dank meme")

        # The Publication looks fine
        self.check_publication(
         "28 September, 1990", "Full Publication | DOI: 10.1002/bip.23067",
         "Marvin Goodwright, Tony Blair, Sam Ireland",
         ["Line 1", "Line 2", "Line 3"]
        )



    def test_cannot_have_missing_id(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no ID
        self.enter_publication(
         "", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no id", error.text.lower())


    def test_cannot_have_invalid_id(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with wrong ID
        self.enter_publication(
         "novel-Meme£", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("£", error.text.lower())


    def test_cannot_have_duplicate_id(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with the ID twice
        self.enter_publication(
         "novel-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )
        self.check_page("/research/novel-meme/")
        self.get("/research/new/")
        self.enter_publication(
         "novel-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("already", error.text.lower())


    def test_cannot_have_missing_title(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no title
        self.enter_publication(
         "new-meme", "", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no title", error.text.lower())


    def test_cannot_have_missing_date(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no date
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", None,
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no date", error.text.lower())


    def test_cannot_have_missing_url(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no url
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", "28-09-1990",
         "", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no url", error.text.lower())


    def test_cannot_have_missing_doi(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no doi
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no doi", error.text.lower())


    def test_cannot_have_missing_authors(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no authors
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "",
         "We report here the isolation of a new meme.",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no authors", error.text.lower())


    def test_cannot_have_missing_abstract(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no abstract
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "",
         "Line 1\n\nLine 2\n\nLine 3"
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no abstract", error.text.lower())


    def test_cannot_have_missing_body(self):
        # User goes to enter new publication
        self.login()
        self.get("/research/new/")

        # They enter a pub with no body
        self.enter_publication(
         "new-meme", "The isolation of a novel dank meme", "28-09-1990",
         "http://journal-of-memology/12345/", "10.1002/bip.23067",
         "Marvin Goodwright, Tony **Blair**, Sam Ireland",
         "We report here the isolation of a new meme.",
         ""
        )

        # They are still on the same page
        self.check_page("/research/new/")

        # There is an error
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertIn("no body", error.text.lower())


    def test_cannot_access_new_research_page_when_not_logged_in(self):
        self.get("/research/new/")
        self.check_page("/")
