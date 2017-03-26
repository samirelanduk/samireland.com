from time import sleep
from .base import FunctionalTest

class BasePageLayoutTests(FunctionalTest):

    def test_base_layout_order(self):
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )


    def test_name_in_header(self):
        self.browser.get(self.live_server_url + "/")
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Sam Ireland", header.text)


    def test_nav_is_unordered_list_of_links(self):
        self.browser.get(self.live_server_url + "/")
        nav = self.browser.find_element_by_tag_name("nav")

        # The only child of the nav is a <ul>
        children = nav.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(3 <= len(children) <= 8)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            self.assertEqual(len(child.find_elements_by_tag_name("a")), 1)


    def test_footer_is_unordered_list_of_img_links(self):
        self.browser.get(self.live_server_url + "/")
        footer = self.browser.find_element_by_tag_name("footer")

        # The only child of the footer is a <ul>
        children = footer.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(2 <= len(children) <= 15)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            links = child.find_elements_by_tag_name("a")
            self.assertEqual(len(links), 1)
            self.assertIsNot(links[0].find_element_by_tag_name("img"), None)



class BasePageStyleTests(FunctionalTest):

    def test_body_detaches_above_1024px(self):
        # On mobile screens the body has no margins
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(body.value_of_css_property("margin"), "0px")

        # As high as 1020px, this is still the case
        self.browser.set_window_size(1020, 800)
        self.assertEqual(body.value_of_css_property("margin"), "0px")

        # But at 1025px, the body detatches
        self.browser.set_window_size(1035, 1000) # Subtract 10px for window frame
        self.assertEqual(body.value_of_css_property("width"), "1024px")
        self.assertEqual(
         body.value_of_css_property("margin-left"),
         body.value_of_css_property("margin-right")
        )
        self.assertNotEqual(body.value_of_css_property("margin-left"), "0px")
        self.assertNotEqual(body.value_of_css_property("margin-top"), "0px")
        self.assertNotEqual(body.value_of_css_property("margin-bottom"), "0px")


    def test_body_has_different_background_to_backdrop(self):
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        backdrop = self.browser.find_element_by_tag_name("html")
        self.assertNotEqual(
         body.value_of_css_property("background-color"),
         backdrop.value_of_css_property("background-color")
        )


    def test_two_different_non_TNR_fonts(self):
        self.browser.get(self.live_server_url + "/")
        header = self.browser.find_element_by_tag_name("header")
        normal_text_div = self.browser.find_element_by_id("brief-summary")
        self.assertNotEqual(
         header.value_of_css_property("font-family"),
         "Times New Roman"
        )
        self.assertNotEqual(
         normal_text_div.value_of_css_property("font-family"),
         "Times New Roman"
        )
        self.assertNotEqual(
         header.value_of_css_property("font-family"),
         normal_text_div.value_of_css_property("font-family")
        )


    def test_header_and_nav_work_on_mobile(self):
        self.browser.get(self.live_server_url + "/")

        # The header is left aligned
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "start"
        )

        # There is a navicon to the right
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(header.location["y"], navicon.location["y"])
        self.assertLess(header.location["x"], navicon.location["x"])

        # The navbar itself isn't displayed
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # Clicking the navicon makes the nav appear
        navicon.click()
        self.assertNotEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # The links are in two columns
        links = navbar.find_elements_by_tag_name("li")
        self.assertEqual(len(set([link.location["x"] for link in links])), 2)

        # Clicking the navicon again makes the nav disappear
        navicon.click()
        sleep(1.5)
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # The user opens the page on an iPad
        self.browser.set_window_size(700, 900)
        self.browser.get(self.live_server_url + "/")

        # The basic layout is still the same
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "start"
        )
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(header.location["y"], navicon.location["y"])
        self.assertLess(header.location["x"], navicon.location["x"])
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # But the links are in three columns now
        navicon.click()
        self.assertNotEqual(
         navbar.value_of_css_property("display"),
         "none"
        )
        links = navbar.find_elements_by_tag_name("li")
        self.assertEqual(len(set([link.location["x"] for link in links])), 3)


    def test_header_and_nav_work_on_desktop(self):
        self.browser.set_window_size(800, 900)
        self.browser.get(self.live_server_url + "/")

        # The header is centred and there is no nav icon
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "center"
        )
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(
         navicon.value_of_css_property("display"),
         "none"
        )

        # The navbar is below it
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertGreater(navbar.location["y"], header.location["y"])

        # The links are all on one row
        links = navbar.find_elements_by_tag_name("li")
        first_link_y = links[0].location["y"]
        for link in links[1:]:
            self.assertEqual(link.location["y"], first_link_y)



class HomePageTests(FunctionalTest):

    def test_can_change_home_page_text(self):
        self.check_can_edit_text("/", "brief-summary", "home")



class AboutPageTests(FunctionalTest):

    def test_about_page_structure(self):
        self.browser.set_window_size(800, 600)
        self.browser.get(self.live_server_url + "/")

        # The last nav link goes to the about page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[-1].click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/about/"
        )

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        about_bio = main.find_element_by_id("about-bio")

        # There is no edit link because they are not logged in
        links = about_bio.find_elements_by_tag_name("a")
        self.assertEqual(len(links),0)



    def test_can_change_about_page_text(self):
        self.check_can_edit_text("/about/", "about-bio", "about")



class ResearchPageTests(FunctionalTest):

    def test_research_page_structure(self):
        self.browser.set_window_size(800, 600)
        self.browser.get(self.live_server_url + "/")

        # The second nav link goes to the research page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[1].click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/research/"
        )

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        research_summary = main.find_element_by_id("research-summary")

        # There is no edit link because they are not logged in
        links = research_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links),0)

        # There is a div for publications
        publications = main.find_element_by_id("publications")
        h2 = publications.find_elements_by_tag_name("h2")
        no_publications = publications.find_element_by_tag_name("p")



    def test_can_change_research_page_text(self):
        self.check_can_edit_text("/research/", "research-summary", "research")



class ProjectPageTests(FunctionalTest):

    def test_project_page_leads_to_piano_project(self):
        self.browser.set_window_size(800, 600)
        self.browser.get(self.live_server_url + "/")

        # The third nav link goes to the project page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[2].click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/projects/"
        )

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        projects_summary = main.find_element_by_id("projects-summary")

        # There is no edit link because they are not logged in
        links = projects_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links), 0)

        # There is a div devoted to the piano project
        piano_section = main.find_element_by_id("piano-project")
        h2 = piano_section.find_element_by_id("h2")
        piano_summary = piano_section.find_element_by_id("piano-project-summary")
        more_piano_link = piano_section.find_elements_by_tag_name("a")[-1]

        # There is no edit link because they are not logged in
        links = piano_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links), 0)

        # They click the link for more information and are taken to piano page
        more_piano_link.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/"
        )

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        piano_description = main.find_element_by_id("piano-description")

        # There is no edit link because they are not logged in
        links = piano_description.find_elements_by_tag_name("a")
        self.assertEqual(len(links), 0)

        # There is also a section for piano progress
        piano_progress = main.find_element_by_id("piano-progress")


    def test_can_change_project_page_text(self):
        self.check_can_edit_text("/projects/", "projects-summary", "projects")


    def test_can_change_piano_summary_text(self):
        self.check_can_edit_text("/projects/", "piano-summary", "piano-brief")


    def test_can_change_piano_description_text(self):
        self.check_can_edit_text(
         "/projects/piano/", "piano-description", "piano-long"
        )


    def test_can_update_piano_progress(self):
        self.login()
        self.browser.get(self.live_server_url)

        # There is a piano link in the header
        header = self.browser.find_element_by_tag_name("header")
        piano_update_link = header.find_element_by_id("piano-update-link")

        # They click it and are taken to the piano update page
        piano_update_link.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/update/"
        )

        # There is a table for practice data, currently empty
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 0)

        # There is a form for adding a new session
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        self.assertEqual(
         date_input.get_attribute("value"),
         datetime.datetime.now().strftime("%Y-%m-%d")
        )
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]

        # User adds 10 minutes for today
        minutes_input.send_keys("10")
        submit.click()

        # He is still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/update/"
        )

         # There is one row now
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 1)

        # The row contains the correct information
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[0].text,
         datetime.datetime.now().strftime("%-d %B, %Y")
        )
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "10"
        )

        # The piano page now says 10 minutes
        self.browser.get(self.live_server_url + "/piano/")
        piano_progress = main.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("10 minutes", first_p.text)

        # The user adds 50 minutes for ages ago
        self.browser.get(self.live_server_url + "/piano/update")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        date_input.send_keys(date.strftime("22092004"))
        minutes_input.send_keys("10")
        submit.click()

        # The new entry is on the table
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 2)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "10"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[1].text,
         "50"
        )

        # The piano page now says 1 hour
        self.browser.get(self.live_server_url + "/piano/")
        piano_progress = main.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("1 hour", first_p.text)

        # The user adds 90 minutes for the far future
        self.browser.get(self.live_server_url + "/piano/update")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        date_input.send_keys(date.strftime("28092090"))
        minutes_input.send_keys("90")
        submit.click()

        # The new entry is on the table
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 2)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "90"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[1].text,
         "10"
        )
        self.assertEqual(
         rows[2].find_elements_by_tag_name("td")[1].text,
         "50"
        )

        # The piano page now says 2.5 hours
        self.browser.get(self.live_server_url + "/piano/")
        piano_progress = main.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("2 hours and 30 minutes", first_p.text)

        # Each of the rows has a delete button on the update page
        self.browser.get(self.live_server_url + "/piano/update")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        for row in rows[::-1]:
            last_cell = self.browser.find_elements_by_tag_name("td")[-1]
            delete_button = last_cell.find_element_by_tag_name("a")
            self.assertEqual(
             delete_button.text,
             "Delete"
            )

        # He deletes one of the sessions
        delete_button.click()

        # Now he is on a deletion page, and is asked if he is sure
        self.assertRegex(
         self.browser.current_url,
         self.live_server_url + r"/piano/delete/\d+/$"
        )
        form = self.browser.find_element_by_tag_name("form")
        warning = form.find_element_by_id("warning")
        self.assertIn(
         "are you sure?",
         warning.text.lower()
        )

        # There is a back to safety link, and a delete button
        back_to_safety = form.find_element_by_tag_name("a")
        delete_button = form.find_elements_by_tag_name("input")[-1]

        # He goes back to safety
        back_to_safety.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/update/"
        )
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 4)

        # He changes his mind and goes back
        delete_button = rows[-1].find_elements_by_tag_name("a")[-1]
        delete_button.click()
        self.assertRegex(
         self.browser.current_url,
         self.live_server_url + r"/piano/delete/\d+/$"
        )
        form = self.browser.find_element_by_tag_name("form")
        delete_button = form.find_elements_by_tag_name("input")[-1]


        # He deletes, and is taken back to the edit page
        delete_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/update/"
        )

        # There are now three rows
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 2)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "90"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[1].text,
         "10"
        )

        # The piano page now says 1 hours 40 mins
        self.browser.get(self.live_server_url + "/piano/")
        piano_progress = main.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("1 hours and 40 minute", first_p.text)


    def test_cannot_post_session_with_no_date(self):
        self.login()

        # He tries to submit a session with no date
        self.browser.get(self.live_server_url + "/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        self.browser.execute_script(
         "document.getElementById('id_date').setAttribute('value', '');"
        )
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        minutes_input.send_keys(10)
        submit.click()

        # It doesn't work
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 0)

        # There is an error message
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(error.text, "You cannot submit a session with no date")


    def test_cannot_post_session_with_no_minutes(self):
        self.login()

        # He tries to submit a session with no minutes
        self.browser.get(self.live_server_url + "/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        submit = form.find_elements_by_tag_name("input")[-1]
        submit.click()

        # It doesn't work
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 0)

        # There is an error message
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(error.text, "You cannot submit a session with no minutes")


    def test_cannot_post_session_with_duplicate_date(self):
        self.login()

        # He submits a post for today
        self.browser.get(self.live_server_url + "/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        minutes_input.send_keys(10)
        submit.click()

        # He tries to submit a session with the same date
        self.browser.get(self.live_server_url + "/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        minutes_input.send_keys(20)
        submit.click()

        # It doesn't work
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 1)

        # There is an error message
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(error.text, "There is already a session for this date")



class AuthTests(FunctionalTest):

    def test_can_login(self):
        self.browser.get(self.live_server_url + "/")

        # The 'l' is a link and it is the only one
        header = self.browser.find_element_by_tag_name("header")
        links = header.find_elements_by_tag_name("a")
        self.assertEqual(links[0].text, "l")
        self.assertEqual(len(links), 1)

        # Clicking it goes to the login page
        links[0].click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/authenticate/"
        )

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
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )

        # There is a logout button
        header = self.browser.find_element_by_tag_name("header")
        logout_link = header.find_elements_by_tag_name("a")[1]
        self.assertEqual(logout_link.text, "Logout")


    def test_incorrect_login(self):
        self.browser.get(self.live_server_url + "/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("badguy1337")
        password_entry.send_keys("h4ck0r")
        submit_button.click()

        # The attempt fails. The user weeps, and vows to turn their life around
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/youshallnotpass/"
        )
        self.assertIn(
         "thus far shall you come, and no farther",
         self.browser.find_element_by_tag_name("main").text.lower()
        )


    def test_can_logout(self):
        self.login()
        self.browser.get(self.live_server_url + "/")

        # There is a logout link
        header = self.browser.find_element_by_tag_name("header")
        logout_link = header.find_elements_by_tag_name("a")[1]

        # They click it
        logout_link.click()

        # They are back on the home page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )

        # There is only one link in the header
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(len(header.find_elements_by_tag_name("a")), 1)


    def test_private_pages_are_private(self):
        private_pages = (
         "/edit/home/",
        )
        for page in private_pages:
            self.browser.get(self.live_server_url + page)
            self.assertEqual(
             self.browser.current_url,
             self.live_server_url + "/"
            )
