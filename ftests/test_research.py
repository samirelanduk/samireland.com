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
        self.check_page("/research/")
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
         publications[0].find_element_by_class_name("date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         publications[1].find_element_by_class_name("pub-title").text,
         "The Middle Paper"
        )
        self.assertEqual(
         publications[1].find_element_by_class_name("date").text,
         "12 April, 2016"
        )
        self.assertEqual(
         publications[2].find_element_by_class_name("pub-title").text,
         "The First Paper"
        )
        self.assertEqual(
         publications[2].find_element_by_class_name("date").text,
         "1 January, 2016"
        )
