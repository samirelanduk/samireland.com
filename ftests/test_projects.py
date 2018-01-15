from django.core.files.uploadedfile import SimpleUploadedFile
from .base import FunctionalTest
from samireland.models import MediaFile

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

        # There's no new project link
        with self.assertRaises(self.NoElement):
            self.browser.find_element_by_id("new-project")

        # There is a web projects section
        web = self.browser.find_element_by_id("web-projects")
        h2 = web.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Web Projects")
        self.assertIn("no web projects", web.text)
        with self.assertRaises(self.NoElement):
            web.find_element_by_class_name("project")

        # There is a python projects section
        python = self.browser.find_element_by_id("python-projects")
        h2 = python.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Python Projects")
        self.assertIn("no python projects", python.text)
        with self.assertRaises(self.NoElement):
            python.find_element_by_class_name("project")

        # There is an other projects section
        other = self.browser.find_element_by_id("other-projects")
        h2 = other.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Other Projects")
        self.assertIn("no other projects", other.text)
        with self.assertRaises(self.NoElement):
            other.find_element_by_class_name("project")


    def test_can_change_projects_page_text(self):
        self.check_editable_text("/projects/", "summary")



class ProjectAdditionTests(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        MediaFile.objects.create(
         name="bogo-icon", mediafile=SimpleUploadedFile("test1.png", b"\x00\x01")
        )


    def test_can_add_project(self):
        self.login()
        self.get("/projects/")

        # There is a link to create a new project
        new_project = self.browser.find_element_by_id("new-project")
        link = new_project.find_element_by_tag_name("a")
        self.click(link)

        # They are on the new project page
        self.check_page("/projects/new/")
        self.check_title("New Project")
        self.check_h1("New Project")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        name_input = form.find_elements_by_tag_name("input")[0]
        image_input = form.find_elements_by_tag_name("input")[1]
        description_input = form.find_element_by_tag_name("textarea")
        category_input = form.find_element_by_tag_name("select")

        # They enter some data and submit
        name_input.send_keys("bojo.com")
        image_input.send_keys("bogo-icon")
        description_input.send_keys("Line 1\n\nLine 2")
        self.select_dropdown(category_input, "web")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the project page and the project is there
        self.check_page("/projects/")
        web = self.browser.find_element_by_id("web-projects")
        self.assertNotIn("no web projects", web.text)
        projects = web.find_elements_by_class_name("project")
        self.assertEqual(len(projects), 1)
        icon = projects[0].find_element_by_class_name("project-image")
        name = projects[0].find_element_by_tag_name("h3")
        description = projects[0].find_element_by_class_name("project-description")
        self.assertEqual(
         icon.get_attribute("src"),
         "{}/{}".format(self.live_server_url, MediaFile.objects.first().mediafile.url)
        )
        self.assertEqual(name.text, "bojo.com")
        paragraphs = description.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2")

        # The others still don't have any
        python = self.browser.find_element_by_id("python-projects")
        self.assertIn("no python projects", python.text)
        with self.assertRaises(self.NoElement):
            python.find_element_by_class_name("project")
        other = self.browser.find_element_by_id("other-projects")
        self.assertIn("no other projects", other.text)
        with self.assertRaises(self.NoElement):
            other.find_element_by_class_name("project")


        # They do it again with an other project
        new_project = self.browser.find_element_by_id("new-project")
        link = new_project.find_element_by_tag_name("a")
        self.click(link)
        form = self.browser.find_element_by_tag_name("form")
        name_input = form.find_elements_by_tag_name("input")[0]
        image_input = form.find_elements_by_tag_name("input")[1]
        description_input = form.find_element_by_tag_name("textarea")
        category_input = form.find_element_by_tag_name("select")
        name_input.send_keys("Crossfit")
        image_input.send_keys("bogo-icon")
        description_input.send_keys("Line A\n\nLine B")
        self.select_dropdown(category_input, "other")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)
        self.check_page("/projects/")
        other = self.browser.find_element_by_id("other-projects")
        self.assertNotIn("no other projects", other.text)
        projects = other.find_elements_by_class_name("project")
        self.assertEqual(len(projects), 1)
        icon = projects[0].find_element_by_class_name("project-image")
        name = projects[0].find_element_by_tag_name("h3")
        description = projects[0].find_element_by_class_name("project-description")
        self.assertEqual(
         icon.get_attribute("src"),
         "{}/{}".format(self.live_server_url, MediaFile.objects.first().mediafile.url)
        )
        self.assertEqual(name.text, "Crossfit")
        paragraphs = description.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line A")
        self.assertEqual(paragraphs[1].text, "Line B")
