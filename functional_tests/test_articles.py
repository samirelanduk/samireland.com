from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class NewArticleTest(FunctionalTest):

    def test_sam_can_post_article(self):
        # Sam checks that there are no articles yet
        self.browser.get(self.live_server_url + "/writing/")
        article_divs = self.browser.find_elements_by_class_name("article-box")
        self.assertEqual(len(article_divs), 0)

        # Sam goes to the new article page
        self.sam_logs_in()
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
        title_entry.send_keys("A Title")
        summary_entry.send_keys("An Intriguing Summary")
        date_entry.send_keys("24012008")
        body_entry.send_keys("The body of the beast.")
        live_box.click()

        # Sam submits and is taken to the writing page
        submit_button.click()
        self.assertEqual(self.current_url, self.live_server_url + "/writing/")

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
        article_divs[0].click()
        title = self.find_element_by_class_name("article-title")
        summary = self.find_element_by_class_name("article-summary")
        date = self.find_element_by_class_name("article-date")
        body = self.find_element_by_class_name("article-body")
        self.assertEqual(title.text, "A Title")
        self.assertEqual(summary.text, "An Intriguing Summary")
        self.assertEqual(date.text, "24 January, 2008")
        self.assertEqual(body.text, "The body of the beast.")
