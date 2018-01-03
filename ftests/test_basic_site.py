from .base import FunctionalTest

class SiteLayoutTests(FunctionalTest):

    def test_page_layout(self):
        # All the right elements are there
        self.get("/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )

        # The header has the name in it
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(header.text, "Sam Ireland")

        # The nav has a list of links
        nav = self.browser.find_element_by_tag_name("nav")
        ul = nav.find_element_by_tag_name("ul")
        links = ul.find_elements_by_tag_name("li")
        self.assertEqual(links[0].text, "Home")
        self.assertEqual(links[1].text, "Research")
        self.assertEqual(links[2].text, "Projects")
        self.assertEqual(links[3].text, "Writing")
        self.assertEqual(links[4].text, "Blog")
        self.assertEqual(links[5].text, "About")

        # The footer has a bunch of icons
        footer = self.browser.find_element_by_tag_name("footer")
        icons = footer.find_elements_by_class_name("social-icon")
        self.assertGreaterEqual(len(icons), 4)



class HomePageTests(FunctionalTest):

    def test_home_page_structure(self):
        # The user goes to the home page
        self.get("/")
        self.check_title("Home")


        # There is an introductory section
        intro = self.browser.find_element_by_class_name("intro")
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("form")


    def test_can_change_home_page_text(self):
        # The user goes to the home page
        self.login()
        self.get("/")
        intro = self.browser.find_element_by_class_name("intro")
        self.assertEqual(len(intro.find_elements_by_tag_name("p")), 0)

        # There is an edit button and hidden textarea
        edit = intro.find_element_by_tag_name("button")
        self.assertEqual(edit.text, "Edit")
        form = intro.find_element_by_tag_name("form")
        self.check_invisible(form)


        # They click it and there is now a textarea
        edit.click()
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("button")
        self.check_visible(form)
        textarea = form.find_element_by_tag_name("textarea")

        # They enter some text and submit
        textarea.send_keys("Home text 1.\n\nHome text 2.")
        submit = intro.find_elements_by_tag_name("input")[-1]
        submit.click()

        # They are on the same page
        self.check_page("/")

        # The text has been saved
        intro = self.browser.find_element_by_class_name("intro")
        paragraphs = intro.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Home text 1.")
        self.assertEqual(paragraphs[1].text, "Home text 2.")
        form = intro.find_element_by_tag_name("form")
        self.check_invisible(form)

        # They decide to edit it again
        edit = intro.find_element_by_tag_name("button")
        edit.click()
        textarea = intro.find_element_by_tag_name("textarea")
        self.assertEqual(
         textarea.get_attribute("value"), "Home text 1.\n\nHome text 2."
        )
        textarea.send_keys("\n\nHome text 3.")
        submit = intro.find_elements_by_tag_name("input")[-1]
        submit.click()

        # It worked
        self.check_page("/")
        intro = self.browser.find_element_by_class_name("intro")
        paragraphs = intro.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0].text, "Home text 1.")
        self.assertEqual(paragraphs[1].text, "Home text 2.")
        self.assertEqual(paragraphs[2].text, "Home text 3.")



class AuthTests(FunctionalTest):

    def test_can_log_in(self):
        self.get("/")

        # The 'l' is a link and it is the only one
        header = self.browser.find_element_by_tag_name("header")
        links = header.find_elements_by_tag_name("a")
        self.assertEqual(links[0].text, "l")
        self.assertEqual(len(links), 1)

        # Clicking it goes to the login page
        self.click(links[0])
        self.check_page("/authenticate/")
        self.check_title("Log In")
        self.check_h1("Log In")

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


    def test_can_prevent_login(self):
        self.get("/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("badguy1337")
        password_entry.send_keys("h4ck0r")
        submit_button.click()

        # The attempt fails.
        self.check_page("/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        error = login_form.find_element_by_class_name("error-message")
        self.assertEqual(error.text, "Nope!")


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
