from selenium import webdriver
from testarsenal import BrowserTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

class FunctionalTest(StaticLiveServerTestCase, BrowserTest):

    def setUp(self):
        self.browser = webdriver.Chrome()
        User.objects.create_user(
         username="testsam",
         password="testpassword"
        )


    def tearDown(self):
        self.browser.close()


    def login(self):
        self.client.login(username="testsam", password="testpassword")
        cookie = self.client.cookies["sessionid"].value
        self.browser.get(self.live_server_url + "/")
        self.browser.add_cookie({
         "name": "sessionid", "value": cookie, "secure": False, "path": "/"
        })
        self.browser.refresh()


    def check_editable_text(self, page, div_name):
        self.login()
        self.get(page)
        div = self.browser.find_element_by_class_name(div_name)
        self.assertEqual(len(div.find_elements_by_tag_name("p")), 0)

        # There is an edit button and hidden textarea
        edit = div.find_element_by_tag_name("button")
        self.assertEqual(edit.text, "Edit")
        form = div.find_element_by_tag_name("form")
        self.check_invisible(form)


        # They click it and there is now a textarea
        edit.click()
        with self.assertRaises(self.NoElement):
            div.find_element_by_tag_name("button")
        self.check_visible(form)
        textarea = form.find_element_by_tag_name("textarea")

        # They enter some text and submit
        textarea.send_keys("Some text 1.\n\nSome text 2.")
        submit = div.find_elements_by_tag_name("input")[-1]
        submit.click()

        # They are on the same page
        self.check_page(page)

        # The text has been saved
        div = self.browser.find_element_by_class_name(div_name)
        paragraphs = div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Some text 1.")
        self.assertEqual(paragraphs[1].text, "Some text 2.")
        form = div.find_element_by_tag_name("form")
        self.check_invisible(form)

        # They decide to edit it again
        edit = div.find_element_by_tag_name("button")
        edit.click()

        # There are no paragraphs
        with self.assertRaises(self.NoElement):
            div.find_element_by_tag_name("p")
        textarea = div.find_element_by_tag_name("textarea")
        self.assertEqual(
         textarea.get_attribute("value"), "Some text 1.\n\nSome text 2."
        )
        textarea.send_keys("\n\nSome text 3.")
        submit = div.find_elements_by_tag_name("input")[-1]
        submit.click()

        # It worked
        self.check_page(page)
        div = self.browser.find_element_by_class_name(div_name)
        paragraphs = div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0].text, "Some text 1.")
        self.assertEqual(paragraphs[1].text, "Some text 2.")
        self.assertEqual(paragraphs[2].text, "Some text 3.")
