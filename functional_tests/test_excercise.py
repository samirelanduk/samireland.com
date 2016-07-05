from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ExcerciseTest(FunctionalTest):

    def add_muscle_group(self, name):
        # Sam goes to the excercise edit page
        self.browser.get(self.live_server_url + "/health/edit/")

        # There is a section on muscle groups
        section = self.browser.find_element_by_id("muscle")
        heading = section.find_elements_by_tag_name("h2")
        self.assertEqual(heading.text, "Muscle Groups")

        # At the end there is a textbox and a button to add a new group
        textbox = section.find_elements_by_tag_name("input")[-2]
        self.assertEqual(textbox.get_attribute("type"), "text")
        submit = section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(textbox.get_attribute("type"), "submit")

        # He enters a new group
        textbox.send_keys(name)
        submit.click()

        # He is still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit"
        )



class MuscleGroupTests(ExcerciseTest):

    def test_can_add_muscle_group(self):
        self.sam_logs_in()

        # Sam adds a new muscle group
        self.add_muscle_group("toes")

        # The muscle group is there
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("musclegroup")
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0], "toes")

        # He adds another
        self.add_muscle_group("eyebrows")

        # There are two muscle groups there now, in alphabetical order
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("musclegroup")
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0], "eyebrows")
        self.assertEqual(groups[1], "toes")
