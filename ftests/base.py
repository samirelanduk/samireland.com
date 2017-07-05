from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
         username="testsam",
         password="testpassword"
        )
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(350, 600)


    def tearDown(self):
        self.browser.quit()


    def login(self):
        self.client.login(username="testsam", password="testpassword")
        cookie = self.client.cookies["sessionid"].value
        self.browser.get(self.live_server_url + "/")
        self.browser.add_cookie({
         "name": "sessionid", "value": cookie, "secure": False, "path": "/"
        })
        self.browser.refresh()


    def get(self, url):
        self.browser.get(self.live_server_url + url)


    def check_page(self, url):
        self.assertEqual(self.browser.current_url, self.live_server_url + url)


    def hover(self, element):
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()


    def check_can_edit_text(self, url, div_name, text_name):
        self.login()
        self.get(url)

        # There is a link to edit text
        main = self.browser.find_element_by_tag_name("main")
        div = main.find_element_by_id(div_name)
        edit_link = div.find_element_by_tag_name("a")

        # Clicking it takes you to the edit page
        edit_link.click()
        self.check_page("/edit/%s/" % text_name)

        # There is a form for entering the text
        form = self.browser.find_element_by_tag_name("form")
        textarea = form.find_element_by_tag_name("textarea")
        self.assertEqual(textarea.get_attribute("value").strip(), "")
        submit_button = form.find_elements_by_tag_name("input")[-1]

        # Text is entered and submitted
        textarea.send_keys("Paragraph 1.\n\nParagraph 2.")
        submit_button.click()

        # The research page has the new text
        self.check_page(url)
        main = self.browser.find_element_by_tag_name("main")
        div = main.find_element_by_id(div_name)
        paragraphs = div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Paragraph 1.")
        self.assertEqual(paragraphs[1].text, "Paragraph 2.")

        # Unhappy, they click the edit link again
        edit_link = div.find_element_by_tag_name("a")
        edit_link.click()
        self.check_page("/edit/%s/" % text_name)

        # The form has the current text in it
        form = self.browser.find_element_by_tag_name("form")
        textarea = form.find_element_by_tag_name("textarea")
        self.assertEqual(
         textarea.get_attribute("value"),
         "Paragraph 1.\n\nParagraph 2."
        )
        submit_button = form.find_elements_by_tag_name("input")[-1]

        # The user changes the text
        textarea.clear()
        textarea.send_keys("Number 1.\n\nNumber 2.\n\nNumber 3.")
        submit_button.click()

        # The research page has the new text
        self.check_page(url)
        main = self.browser.find_element_by_tag_name("main")
        div = main.find_element_by_id(div_name)
        paragraphs = div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0].text, "Number 1.")
        self.assertEqual(paragraphs[1].text, "Number 2.")
        self.assertEqual(paragraphs[2].text, "Number 3.")
