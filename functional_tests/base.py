from selenium import webdriver
import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_url = "http://" + arg.split("=")[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def sam_logs_in(self):
        # Sam goes to the login page
        self.browser.get(self.server_url + "/login/")

        # He logs in
        name_entry = self.browser.find_element_by_id("name_entry")
        password_entry = self.browser.find_element_by_id("password_entry")
        submit_button = self.browser.find_element_by_id("submit_button")
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
         self.find_element_by_tag_name("header").text
        )


    def sam_logs_out(self):
        # Sam goes to the login page
        self.browser.get(self.server_url + "/logout/")

        # He is asked if he would like to logout
        self.assertIn(
         "would you like to logout?",
         self.browser.find_element_by_tag_name("main").text.lower(),
        )

        # He says no
        no_button = self.browser.find_element_by_tag_name("button")
        no_button.click()

        # He is on the home page, and he is still logged in
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.assertIn(
         "logged in",
         self.find_element_by_tag_name("header").text
        )

        # He changes his mind
        self.browser.get(self.server_url + "/logout/")
        yes_button = self.browser.find_element_by_tag_name("input")
        yes_button.click()

        # He is on the home page, logged out
        self.assertEqual(
         self.browser.current_url,
         self.server_url + "/"
        )
        self.assertNotIn(
         "logged in",
         self.find_element_by_tag_name("header").text
        )
