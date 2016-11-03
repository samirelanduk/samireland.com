import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
         username="person",
         password="secret"
        )
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def sam_logs_in(self):
        # Sam goes to the login page
        self.browser.get(self.live_server_url + "/account/login/")

        # He logs in
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("person")
        password_entry.send_keys("secret")
        submit_button.click()

        # He is on the home page, but he can see he is logged in
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        for required_text in ["Logout", "Piano", "New Blog", "Edit Blog"]:
            self.assertIn(
             required_text,
             self.browser.find_element_by_tag_name("header").text
            )


    def sam_logs_out(self):
        # Sam goes to the logout page
        self.browser.get(self.live_server_url + "/account/logout/")

        # He is on the home page, logged out
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.assertNotIn(
         "logout",
         self.browser.find_element_by_tag_name("header").text.lower()
        )
