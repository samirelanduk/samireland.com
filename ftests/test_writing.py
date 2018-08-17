from .base import FunctionalTest
from samireland.models import Article

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


    def test_writing_page_articles(self):
        Article.objects.create(
         id="article-1", title="The First Article", date="2016-01-01",
         summary="summary1", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-2", title="The Recent Article", date="2016-08-09",
         summary="summary2", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-3", title="The Middle Article", date="2016-04-12",
         summary="summary3", body="Line 1\n\nLine 2"
        )

        # They go to the page and look at the articles - there are 3
        self.get("/writing/")
        articles = self.browser.find_element_by_id("articles")
        articles = articles.find_elements_by_class_name("article")
        self.assertEqual(len(articles), 3)

        # They are in the correct order
        self.assertEqual(
         articles[0].find_element_by_class_name("article-title").text,
         "The Recent Article"
        )
        self.assertEqual(
         articles[0].find_element_by_class_name("date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         articles[1].find_element_by_class_name("article-title").text,
         "The Middle Article"
        )
        self.assertEqual(
         articles[1].find_element_by_class_name("date").text,
         "12 April, 2016"
        )
        self.assertEqual(
         articles[2].find_element_by_class_name("article-title").text,
         "The First Article"
        )
        self.assertEqual(
         articles[2].find_element_by_class_name("date").text,
         "1 January, 2016"
        )
