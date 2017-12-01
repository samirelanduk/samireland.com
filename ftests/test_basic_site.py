from .base import FunctionalTest

class SiteLayoutTests(FunctionalTest):

    def test_page_layout(self):
        # All the right elements are there
        self.get("/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )
