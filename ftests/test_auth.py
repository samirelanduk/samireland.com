"""Contains tests of authentication and logging in."""

from time import sleep
from .base import FunctionalTest

class LoginTests(FunctionalTest):

    def test_can_login(self):
        self.get("/")

        # The 'l' is a link and it is the only one
        header = self.browser.find_element_by_tag_name("header")
        links = header.find_elements_by_tag_name("a")
        self.assertEqual(links[0].text, "l")
        self.assertEqual(len(links), 1)

        # Clicking it goes to the login page
        links[0].click()
        self.check_page("/authenticate/")

        # There is a login form
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]

        # They login
        name_entry.send_keys("testsam")
        password_entry.send_keys("testpassword")
        submit_button.click()

        # They are on the home page
        self.check_page("/")

        # There is a logout button
        header = self.browser.find_element_by_tag_name("header")
        logout_link = header.find_elements_by_tag_name("a")[-1]
        self.assertEqual(logout_link.text, "Logout")


    def test_incorrect_login(self):
        self.get("/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("badguy1337")
        password_entry.send_keys("h4ck0r")
        submit_button.click()

        # The attempt fails. The user weeps, and vows to turn their life around
        self.check_page("/youshallnotpass/")
        self.assertIn(
         "thus far shall you come, and no farther",
         self.browser.find_element_by_tag_name("main").text.lower()
        )



class LogOutTests(FunctionalTest):

    def test_can_logout(self):
        self.login()
        self.get("/")

        # There is a logout link
        header = self.browser.find_element_by_tag_name("header")
        logout_link = header.find_elements_by_tag_name("a")[-1]

        # They click it
        logout_link.click()

        # They are back on the home page
        self.check_page("/")

        # There is only one link in the header
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(len(header.find_elements_by_tag_name("a")), 1)
