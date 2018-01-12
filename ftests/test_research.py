from .base import FunctionalTest

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
        body_input = form.find_elements_by_tag_name("textarea")[1]
