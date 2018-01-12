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
        publications = self.browser.find_element_by_class_name("publications")
        h2 = publications.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Publications")
        self.assertIn("no publications", publications.text)


    def test_can_change_research_page_text(self):
        self.check_editable_text("/research/", "summary")
