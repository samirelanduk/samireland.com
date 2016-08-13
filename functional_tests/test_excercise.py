from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time

class ExcerciseTest(FunctionalTest):

    def add_muscle_group(self, name):
        # Sam goes to the excercise edit page
        self.browser.get(self.live_server_url + "/health/edit/")

        # There is a section on muscle groups
        section = self.browser.find_element_by_id("muscle")
        heading = section.find_element_by_tag_name("h2")
        self.assertEqual(heading.text, "Muscle Groups")

        # At the end there is a textbox and a button to add a new group
        textbox = section.find_elements_by_tag_name("input")[-2]
        self.assertEqual(textbox.get_attribute("type"), "text")
        submit = section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(submit.get_attribute("type"), "submit")

        # He enters a new group
        textbox.send_keys(name)
        submit.click()

        # He is still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit/"
        )



class MuscleGroupTests(ExcerciseTest):

    def test_can_add_muscle_group(self):
        self.sam_logs_in()

        # Sam adds a new muscle group
        self.add_muscle_group("toes")

        # The muscle group is there
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].text, "toes")

        # He adds another
        self.add_muscle_group("eyebrows")

        # There are two muscle groups there now, in alphabetical order
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].text, "eyebrows")
        self.assertEqual(groups[1].text, "toes")


    def test_can_delete_muscle_group(self):
        # Sam adds three muscle groups
        self.add_muscle_group("shoulders")
        self.add_muscle_group("knees")
        self.add_muscle_group("toes")

        # The three groups are on the edit page
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0].text, "knees")
        self.assertEqual(groups[1].text, "shoulders")
        self.assertEqual(groups[2].text, "toes")

        # He clicks the shoulders text and is taken to its page
        groups[1].find_element_by_tag_name("a").click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit/musclegroup/shoulders/"
        )
        self.assertEqual(
         self.browser.find_element_by_tag_name("h1").text,
         "shoulders"
        )

        # There is a button to delete the group
        delete = self.browser.find_element_by_id("delete-button")
        delete.click()

        # He is on a page asking him if he is sure
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit/musclegroup/shoulders/delete/"
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
         self.live_server_url + "/health/edit/musclegroup/shoulders/"
        )

        # He changes his mind and goes back
        delete = self.browser.find_element_by_id("delete-button")
        delete.click()

        # He deletes, and is taken back to the edit page
        form = self.browser.find_element_by_tag_name("form")
        delete_button = form.find_elements_by_tag_name("input")[-1]
        delete_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit"
        )

        # The group is gone
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0], "knees")
        self.assertEqual(groups[1], "toes")


    def test_can_modify_muscle_group_name(self):
        # Sam adds three muscle groups
        self.add_muscle_group("shoulders")
        self.add_muscle_group("knees")
        self.add_muscle_group("toes")

        # The three groups are on the edit page
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0].text, "knees")
        self.assertEqual(groups[1].text, "shoulders")
        self.assertEqual(groups[2].text, "toes")

        # He clicks the shoulders text and is taken to its page
        groups[1].click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit/musclegroup/shoulders/"
        )
        self.assertEqual(
         self.browser.find_element_by_tag_name("h1").text,
         "shoulders"
        )

        # There is a section to change the name
        new_name = self.browser.find_element_by_id("editname")
        textbox = new_name.find_elements_by_tag_name("input")[0]
        self.assertEqual(textbox.get_attribute("type"), "text")
        submit = section.find_elements_by_tag_name("input")[1]
        self.assertEqual(textbox.get_attribute("type"), "submit")

        # He changes the name to 'neck'
        textbox.send_keys("neck")
        submit.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/health/edit/musclegroup/neck/"
        )
        self.assertEqual(
         self.browser.find_element_by_tag_name("h1").text,
         "neck"
        )

        # The name has changed on the edit page too
        self.browser.get(self.live_server_url + "/health/edit/")
        section = self.browser.find_element_by_id("muscle")
        groups = section.find_elements_by_class_name("muscle-group")
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0], "knees")
        self.assertEqual(groups[1], "neck")
        self.assertEqual(groups[2], "toes")
