from selenium import webdriver
from .base import SamTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class KeepOut(SamTest):

    def test_cannot_access_protected_pages(self):
        # A crafty user has been perusing GitHub and has found the secret URLs
        # They try to create a new post, but fail
        self.browser.get(self.live_server_url + "/blog/new/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )

        # Unperturbed, the dastardly user tried to access other pages
        self.browser.get(self.live_server_url + "/blog/edit/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.browser.get(self.live_server_url + "/blog/edit/1/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.browser.get(self.live_server_url + "/blog/delete/1/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.browser.get(self.live_server_url + "/logout/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )


    def test_login_attempt_fails(self):
        # Utterly demoralised, the user decides to try and login
        self.browser.get(self.live_server_url + "/login/")
        name_entry = self.browser.find_element_by_id("name_entry")
        password_entry = self.browser.find_element_by_id("password_entry")
        submit_button = self.browser.find_element_by_id("submit_button")
        name_entry.send_keys("badguy")
        password_entry.send_keys("swordfish")
        submit_button.click()

        # The attempt fails
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/login/fail"
        )
        self.assertIn(
         "thus far have you come, and no further",
         self.browser.find_element_by_tag_name("main").text.lower()
        )

        # The user weeps, and vows to turn their life around



class LetIn(SamTest):

    def test_can_login(self):
        self.sam_logs_in()


    def test_can_access_blog_pages(self):
        # Sam logs in
        self.sam_logs_in()

        # Sam goes to the new post page
        self.browser.get(self.live_server_url + "/blog/new/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/new/"
        )

        # Sam goes to the edit posts page
        self.browser.get(self.live_server_url + "/blog/edit/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/edit/"
        )

    def test_can_logout(self):
        self.sam_logs_in()
        self.sam_logs_out()
