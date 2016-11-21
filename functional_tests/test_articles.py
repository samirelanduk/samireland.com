from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ArticleTest(FunctionalTest):

    def sam_writes_article(self, title, summary, date, body, visible):
        # Sam goes to the new article page
        self.browser.get(self.live_server_url + "/writing/new/")

        # There is a form for entering a article
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        summary_entry = form.find_elements_by_tag_name("input")[1]
        date_entry = form.find_elements_by_tag_name("input")[2]
        body_entry = form.find_element_by_tag_name("textarea")
        live_box = form.find_elements_by_tag_name("input")[3]
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.assertEqual(title_entry.get_attribute("type"), "text")
        self.assertEqual(summary_entry.get_attribute("type"), "text")
        self.assertEqual(date_entry.get_attribute("type"), "date")
        self.assertEqual(live_box.get_attribute("type"), "checkbox")

        # Sam write an article
        title_entry.send_keys(title)
        summary_entry.send_keys(summary)
        date_entry.send_keys(date)
        body_entry.send_keys(body)
        if (live_box.is_selected() and not visible) or (not live_box.is_selected() and visible):
            live_box.click()

        # Sam submits and is taken to the writing page
        submit_button.click()
        self.assertEqual(self.current_url, self.live_server_url + "/writing/")



class NewArticleTest(FunctionalTest):

    def test_sam_can_post_article(self):
        # Sam checks that there are no articles yet
        self.browser.get(self.live_server_url + "/writing/")
        article_divs = self.browser.find_elements_by_class_name("article-box")
        self.assertEqual(len(article_divs), 0)

        # Sam writes an article
        self.sam_logs_in()
        self.sam_writes_article(
         "A Title",
         "An Intriguing Summary",
         "24012008",
         "The body of the beast.",
         True
        )

        # There is the article
        article_divs = self.browser.find_elements_by_class_name("article-box")
        self.assertEqual(len(article_divs), 1)
        self.assertEqual(
         article_divs[0].find_element_by_tag_name("article-box-title").text,
         "A Title"
        )
        self.assertEqual(
         article_divs[0].find_element_by_tag_name("article-box-summary").text,
         "An Intriguing Summary"
        )
        self.assertEqual(
         article_divs[0].find_element_by_tag_name("article-box-summary").text,
         "24 January, 2008"
        )

        # Sam clicks it and is taken to the article
        article_divs[0].find_element_by_tag_name("article-box-title").click()
        title = self.find_element_by_class_name("article-title")
        summary = self.find_element_by_class_name("article-summary")
        date = self.find_element_by_class_name("article-date")
        body = self.find_element_by_class_name("article-body")
        self.assertEqual(title.text, "A Title")
        self.assertEqual(summary.text, "An Intriguing Summary")
        self.assertEqual(date.text, "24 January, 2008")
        self.assertEqual(body.text, "The body of the beast.")


    def test_new_article_appears_on_home_page(self):
        # Sam writes an excellent article
        self.sam_logs_in()
        self.sam_writes_article("Title", "Summary", "01012001", "Main", True)

        # He goes to the main page and there is the article summary
        self.browser.get(self.live_server_url + "/")
        latest_writing = self.browser.find_element_by_id("latest_writing")
        article_div = latest_writing.find_element_by_class_name("article-box")
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-title").text,
         "Title"
        )
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-summary").text,
         "Summary"
        )
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-summary").text,
         "1 January, 2001"
        )

        # He clicks it and is taken to the article
        article_div.find_element_by_tag_name("article-box-title").click()
        title = self.find_element_by_class_name("article-title")
        summary = self.find_element_by_class_name("article-summary")
        date = self.find_element_by_class_name("article-date")
        body = self.find_element_by_class_name("article-body")
        self.assertEqual(title.text, "Title")
        self.assertEqual(summary.text, "Summary")
        self.assertEqual(date.text, "1 January, 2001")
        self.assertEqual(body.text, "Body")


    def test_can_write_multiple_articles(self):
        # Sam writes multiple excellent articles
        self.sam_logs_in()
        self.sam_writes_article("Title4", "Summary4", "01012004", "Main4", True)
        self.sam_writes_article("Title2", "Summary2", "01012002", "Main2", True)
        self.sam_writes_article("Title1", "Summary1", "01012001", "Main1", True)
        self.sam_writes_article("Title5", "Summary5", "01012005", "Main5", True)
        self.sam_writes_article("Title3", "Summary3", "01012003", "Main3", True)

        # They are on the writing page, in order of date
        self.browser.get(self.live_server_url + "/writing/")
        article_divs = self.browser.find_elements_by_class_name("article-box")
        self.assertEqual(len(article_divs), 5)
        self.assertEqual(
         article_divs[0].find_element_by_tag_name("article-box-title").text,
         "Title5"
        )
        self.assertEqual(
         article_divs[1].find_element_by_tag_name("article-box-title").text,
         "Title4"
        )
        self.assertEqual(
         article_divs[2].find_element_by_tag_name("article-box-title").text,
         "Title3"
        )
        self.assertEqual(
         article_divs[3].find_element_by_tag_name("article-box-title").text,
         "Title2"
        )
        self.assertEqual(
         article_divs[4].find_element_by_tag_name("article-box-title").text,
         "Title1"
        )


    def test_most_recent_article_is_on_main_page(self):
        # Sam writes multiple excellent articles
        self.sam_logs_in()
        self.sam_writes_article("Title4", "Summary4", "01012004", "Main4", True)
        self.sam_writes_article("Title2", "Summary2", "01012002", "Main2", True)
        self.sam_writes_article("Title1", "Summary1", "01012001", "Main1", True)
        self.sam_writes_article("Title5", "Summary5", "01012005", "Main5", True)
        self.sam_writes_article("Title3", "Summary3", "01012003", "Main3", True)

        # Sam finds the most recent article on the main page
        self.browser.get(self.live_server_url + "/")
        latest_writing = self.browser.find_element_by_id("latest_writing")
        article_div = latest_writing.find_element_by_class_name("article-box")
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-title").text,
         "Title5"
        )
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-summary").text,
         "Summar5"
        )
        self.assertEqual(
         article_div.find_element_by_tag_name("article-box-summary").text,
         "5 January, 2001"
        )
