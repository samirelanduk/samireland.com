from .base import FunctionalTest
from samireland.models import Publication

class ResearchPageTests(FunctionalTest):

    def test_research_page_layout(self):
        # The user goes to the research page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[1])

        # The page has the correct heading
        self.check_title("Research")
        self.check_h1("Research")

        # There's some summary text
        summary = self.browser.find_element_by_class_name("summary")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("form")

        # There is a publications section
        publications = self.browser.find_element_by_id("publications")
        h2 = publications.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Publications")
        self.assertIn("no publications", publications.text)
        with self.assertRaises(self.NoElement):
            publications.find_element_by_tag_name("a")


    def test_can_change_research_page_text(self):
        self.check_editable_text("/research/", "summary")


    def test_research_page_publications(self):
        Publication.objects.create(
         id="paper-1", title="The First Paper", date="2016-01-01",
         url="www.com", doi="DDD", authors="Jack, Jill",
         body="Line 1\n\nLine 2"
        )
        Publication.objects.create(
         id="paper-2", title="The Recent Paper", date="2016-08-09",
         url="www.com", doi="DDD2", authors="Jack, Jill, Bob",
         body="Line 1\n\nLine 2"
        )
        Publication.objects.create(
         id="paper-3", title="The Middle Paper", date="2016-04-12",
         url="www.com", doi="DDD3", authors="Jack, Sally",
         body="Line 1\n\nLine 2"
        )

        # They go to the page and look at the publications - there are 3
        self.get("/research/")
        publications = self.browser.find_element_by_id("publications")
        publications = publications.find_elements_by_class_name("publication")
        self.assertEqual(len(publications), 3)

        # They are in the correct order
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-title").text,
         "The Recent Paper"
        )
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         publications[1].find_element_by_class_name("pub-title").text,
         "The Middle Paper"
        )
        self.assertEqual(
         publications[1].find_element_by_class_name("pub-date").text,
         "12 April, 2016"
        )
        self.assertEqual(
         publications[2].find_element_by_class_name("pub-title").text,
         "The First Paper"
        )
        self.assertEqual(
         publications[2].find_element_by_class_name("pub-date").text,
         "1 January, 2016"
        )



class PublicationAdditionTests(FunctionalTest):

    def test_can_add_publication(self):
        self.login()
        self.get("/research/")

        # There is a link to create a new publication
        publications = self.browser.find_element_by_id("publications")
        link = publications.find_element_by_tag_name("a")
        self.click(link)

        # They are on the new publication page
        self.check_page("/research/new/")
        self.check_title("New Publication")
        self.check_h1("New Publication")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        body_input = form.find_elements_by_tag_name("textarea")[0]

        # They enter some data and submit
        id_input.send_keys("my-first-paper")
        title_input.send_keys("My First Paper")
        date_input.send_keys("01-06-2017")
        url_input.send_keys("https://papers.com/23/")
        doi_input.send_keys("10.1038/171737a0")
        authors_input.send_keys("S Ireland, M *Good*wright")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the page for the new publication
        self.check_page("/research/my-first-paper/")
        self.check_title("My First Paper")
        self.check_h1("My First Paper")

        # There is an about section
        about = self.browser.find_element_by_class_name("pub-about")
        date = about.find_element_by_class_name("date")
        link = about.find_element_by_class_name("external-link")
        authors = about.find_element_by_class_name("authors")
        self.assertEqual(date.text, "1 June, 2017")
        self.assertEqual(link.text, "Full Publication | DOI: 10.1038/171737a0")
        self.assertEqual(authors.text, "S Ireland, M Goodwright")

        # There is a body
        body = self.browser.find_element_by_class_name("pub-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2")

        # They go back to the research page and the publication is there too
        self.get("/research/")
        publications = self.browser.find_element_by_id("publications")
        self.assertNotIn("no publications", publications.text)
        publications = publications.find_elements_by_class_name("publication")
        self.assertEqual(len(publications), 1)
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-title").text,
         "My First Paper"
        )
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-date").text,
         "1 June, 2017"
        )
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-authors").text,
         "S Ireland, M Goodwright"
        )
        self.assertEqual(
         publications[0].find_element_by_class_name("pub-summary").text,
         "Read Summary"
        )
        self.click(publications[0].find_element_by_tag_name("a"))
        self.check_page("/research/my-first-paper/")


    def test_publication_id_must_be_unique(self):
        self.login()
        self.get("/research/new/")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        body_input = form.find_elements_by_tag_name("textarea")[0]

        # They enter some data and submit
        id_input.send_keys("my-first-paper")
        title_input.send_keys("My First Paper")
        date_input.send_keys("01-06-2017")
        url_input.send_keys("https://papers.com/23/")
        doi_input.send_keys("10.1038/171737a0")
        authors_input.send_keys("S Ireland, M *Good*wright")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They do it again
        self.get("/research/new/")
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        id_input.send_keys("my-first-paper")
        title_input.send_keys("My First Paper")
        date_input.send_keys("01-06-2017")
        url_input.send_keys("https://papers.com/23/")
        doi_input.send_keys("10.1038/171737a0")
        authors_input.send_keys("S Ireland, M *Good*wright")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the same page
        self.check_page("/research/new/")

        # The form is still filled in
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        self.assertEqual(id_input.get_attribute("value"), "my-first-paper")
        self.assertEqual(title_input.get_attribute("value"), "My First Paper")
        self.assertEqual(date_input.get_attribute("value"), "2017-06-01")
        self.assertEqual(url_input.get_attribute("value"), "https://papers.com/23/")
        self.assertEqual(doi_input.get_attribute("value"), "10.1038/171737a0")
        self.assertEqual(authors_input.get_attribute("value"), "S Ireland, M *Good*wright")
        self.assertEqual(body_input.get_attribute("value"), "Line 1\n\nLine 2")

        # There is an error message
        error = form.find_element_by_class_name("error-message")
        self.assertIn("already", error.text)



class PublicationEditingTests(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        Publication.objects.create(
         id="paper-1", title="The First Paper", date="2016-01-01",
         url="www.com", doi="DDD", authors="Jack, Jill",
         body="Line 1\n\nLine 2"
        )


    def test_can_edit_paper(self):
        self.login()

        # The user goes to the publication page
        self.get("/research/paper-1/")

        # There is an edit link
        edit = self.browser.find_element_by_class_name("edit")
        self.click(edit)

        # They are on the edit page, and there is a filled in form
        self.check_page("/research/paper-1/edit/")
        self.check_title("Edit Publication")
        self.check_h1("Edit Publication")
        form = self.browser.find_element_by_tag_name("form")
        id_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        date_input = form.find_elements_by_tag_name("input")[2]
        url_input = form.find_elements_by_tag_name("input")[3]
        doi_input = form.find_elements_by_tag_name("input")[4]
        authors_input = form.find_elements_by_tag_name("input")[5]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        self.assertEqual(id_input.get_attribute("value"), "paper-1")
        self.assertFalse(id_input.is_enabled())
        self.assertEqual(title_input.get_attribute("value"), "The First Paper")
        self.assertEqual(date_input.get_attribute("value"), "2016-01-01")
        self.assertEqual(url_input.get_attribute("value"), "www.com")
        self.assertEqual(doi_input.get_attribute("value"), "DDD")
        self.assertEqual(authors_input.get_attribute("value"), "Jack, Jill")
        self.assertEqual(body_input.get_attribute("value"), "Line 1\n\nLine 2")

        # They make a bunch of edits and save
        title_input.send_keys("T")
        date_input.send_keys("2")
        url_input.send_keys("U")
        doi_input.send_keys("D")
        authors_input.send_keys("A")
        body_input.send_keys("B")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the publication page and it is changed
        self.check_page("/research/paper-1/")
        self.check_title("The First PaperT")
        self.check_h1("The First PaperT")
        about = self.browser.find_element_by_class_name("pub-about")
        date = about.find_element_by_class_name("date")
        link = about.find_element_by_class_name("external-link")
        authors = about.find_element_by_class_name("authors")
        self.assertEqual(date.text, "2 January, 2016")
        self.assertEqual(link.text, "Full Publication | DOI: DDDD")
        self.assertEqual(authors.text, "Jack, JillA")

        # There is a body
        body = self.browser.find_element_by_class_name("pub-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2B")
