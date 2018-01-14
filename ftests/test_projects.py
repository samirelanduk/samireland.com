from .base import FunctionalTest

class ProjectPageTests(FunctionalTest):

    def test_project_page_layout(self):
        # The user goes to the project page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[2])

        # The page has the correct heading
        self.check_page("/projects/")
        self.check_title("Projects")
        self.check_h1("Projects")

        # There's some summary text
        summary = self.browser.find_element_by_class_name("summary")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            summary.find_element_by_tag_name("form")

        # There is a web projects section
        web = self.browser.find_element_by_id("web-projects")
        h2 = web.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Web Projects")
        self.assertIn("no web projects", web.text)
        with self.assertRaises(self.NoElement):
            web.find_element_by_tag_name("a")

        # There is a python projects section
        python = self.browser.find_element_by_id("python-projects")
        h2 = python.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Python Projects")
        self.assertIn("no python projects", python.text)
        with self.assertRaises(self.NoElement):
            python.find_element_by_tag_name("a")

        # There is an other projects section
        other = self.browser.find_element_by_id("other-projects")
        h2 = other.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Other Projects")
        self.assertIn("no other projects", other.text)
        with self.assertRaises(self.NoElement):
            other.find_element_by_tag_name("a")


    def test_can_change_projects_page_text(self):
        self.check_editable_text("/projects/", "summary")
