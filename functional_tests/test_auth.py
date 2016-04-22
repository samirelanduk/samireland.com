from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class KeepOut(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


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
        self.browser.get(self.live_server_url + "/blog/edit/1")
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )
        self.browser.get(self.live_server_url + "/blog/delete/1")
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
         self.browser.find_elements_by_tag_name("main").text.lower()
        )

        # The user weeps, and vows to turn their life around
