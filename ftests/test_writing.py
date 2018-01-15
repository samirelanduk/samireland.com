from .base import FunctionalTest

class WritingPageTests(FunctionalTest):

    def test_writing_page_layout(self):
        # The user goes to the writing page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[3])

        # The page has the correct heading
        self.check_page("/writing/")
        self.check_title("Writing")
        self.check_h1("Writing")

        # There's some summary text
        summary = self.browser.find_element_by_class_name("summary")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("form")

        # There is a writing section
        articles = self.browser.find_element_by_id("articles")
        self.assertIn("no articles", articles.text)
        with self.assertRaises(self.NoElement):
            articles.find_element_by_tag_name("a")
