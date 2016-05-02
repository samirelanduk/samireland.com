from selenium import webdriver
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base import FunctionalTest

class KeepOut(FunctionalTest):

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
        self.browser.get(self.live_server_url + "/media/")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.browser.get(self.live_server_url + "/media/upload/")
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
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = form.find_elements_by_tag_name("input")[0]
        password_entry = form.find_elements_by_tag_name("input")[1]
        submit_button = form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("badguy1337")
        password_entry.send_keys("h4ck0r")
        submit_button.click()

        # The attempt fails. The user weeps, and vows to turn their life around
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/login/fail/"
        )
        self.assertIn(
         "thus far have you come, and no further",
         self.browser.find_element_by_tag_name("main").text.lower()
        )


@skip
class LetIn(FunctionalTest):

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
