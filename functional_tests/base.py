import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def sam_logs_in(self):
        # Sam goes to the login page
        self.browser.get(self.live_server_url + "/login/")

        # He logs in
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = form.find_elements_by_tag_name("input")[0]
        password_entry = form.find_elements_by_tag_name("input")[1]
        submit_button = form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("sam")
        password_entry.send_keys("testpassword")
        submit_button.click()

        # He is on the home page, but he can see he is logged in
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.assertIn(
         "logged in",
         self.find_element_by_tag_name("header").text.lower()
        )


    def sam_logs_out(self):
        # Sam goes to the login page
        self.browser.get(self.server_url + "/logout/")

        # He is asked if he would like to logout
        form = self.browser.find_elements_by_tag_name("form")
        self.assertIn(
         "would you like to logout?",
         form.text.lower(),
        )

        # He says no
        no_button = form.find_element_by_tag_name("a")
        no_button.click()

        # He is on the home page, and he is still logged in
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.assertIn(
         "logged in",
         self.find_element_by_tag_name("header").text.lower()
        )

        # He changes his mind
        self.browser.get(self.server_url + "/logout/")
        form = self.browser.find_elements_by_tag_name("form")
        yes_button = form.find_element_by_tag_name("input")
        yes_button.click()

        # He is on the home page, logged out
        self.assertEqual(
         self.browser.current_url,
         self.server_url + "/"
        )
        self.assertNotIn(
         "logged in",
         self.find_element_by_tag_name("header").text.lower()
        )
