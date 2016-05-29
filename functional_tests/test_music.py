import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class MusicContentTest(FunctionalTest):

    def test_main_music_page_looks_right(self):
        # The user goes to the music page
        self.browser.get(self.live_server_url + "/music/")

        # 'Learning Piano' is in the header, and the title
        self.assertIn("Learning Piano", self.browser.title)
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Learning Piano", header.text)

        # There is some explanatory text
        explanation = self.browser.find_element_by_id("explanation")
        self.assertGreater(
         len(explanation.find_elements_by_tag_name("p")),
         5
        )

        # There are two videos on the page - the intro and the most recent one
        youtube_urls = [frame.get_attribute("src").split("/")[-1] for
         frame in self.browser.find_elements_by_tag_name("iframe")]
        self.assertIn("zgfARa9usiw", youtube_urls)
        self.browser.get(
         "https://www.youtube.com/channel/UCILeIbhtlv4lmgAaZbPKr8A"
        )
        latest_url = self.browser.find_element_by_class_name(
         "yt-lockup-title").find_element_by_tag_name(
          "a").get_attribute("href").split("=")[-1]
        self.assertIn(latest_url, youtube_urls)


    def test_main_music_page_graphs(self):
        # The user goes to the music page
        self.browser.get(self.live_server_url + "/music/")

        # There is a section on practice progress
        progress = self.browser.find_element_by_id("progress")
        self.assertEqual(
         progress.find_element_by_tag_name("h2").text,
         "Progress"
        )

        # There is a sub-section on the past month
        past_thirty = progress.find_element_by_id("month")
        self.assertEqual(
         past_thirty.find_element_by_tag_name("h3").text,
         "Past Thirty Days"
        )
        charts = past_thirty.find_elements_by_class_name("charts")
        self.assertEqual(len(charts), 2)
        for chart in charts:
            self.assertIsNot(chart.find_element_by_tag_name("svg"), None)

        # There is a sub-section on the past year
        past_year = progress.find_element_by_id("year")
        self.assertEqual(
         past_year.find_element_by_tag_name("h3").text,
         "Past Twelve Months"
        )
        charts = past_year.find_elements_by_class_name("charts")
        self.assertEqual(len(charts), 2)
        for chart in charts:
            self.assertIsNot(chart.find_element_by_tag_name("svg"), None)



class PracticeAppTest(FunctionalTest):

    def test_can_practice_notes(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/music/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The first option is notes - they click it
        self.assertEqual(
         options[0].find_elements_by_tag_name("label").text,
         "Notes"
        )
        options[0].find_elements_by_tag_name("input").click()

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id(
         "seconds").find_elements_by_tag_name("input")
        seconds.send_keys("1")

        # They start the practice
        start = self.browser.find_element_by_tag_name("button")
        display = self.browser.find_element_by_id("display")
        self.assertEqual(display.text, "")
        start.click()

        # They go for ten seconds
        note = display.text
        allowed_values = [
         "A", "B", "C", "D", "E", "F", "G",
         "A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"
        ]
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(1)
            next_note = display.text
            self.assertNotEqual(note, next_note)
            note = next_note

        # It's too much - they try again at two seconds
        stop = self.browser.find_elemenst_by_tag_name[1]("button")
        stop.click()
        self.assertEqual(display.text, "")
        seconds.send_keys("2")
        start.click()
        note = display.text
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(1)
            next_note = display.text
            self.assertNotEqual(note, next_note)
            note = next_note


    def test_can_practice_chords(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/music/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The second option is chords - they click it
        self.assertEqual(
         options[1].find_elements_by_tag_name("label").text,
         "Chords"
        )
        options[0].find_elements_by_tag_name("input").click()

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id(
         "seconds").find_elements_by_tag_name("input")
        seconds.send_keys("1")

        # They start the practice
        start = self.browser.find_element_by_tag_name("button")
        display = self.browser.find_element_by_id("display")
        self.assertEqual(display.text, "")
        start.click()

        # They go for ten seconds
        chord = display.text
        allowed_values = [
         "A Major", "B Major", "C Major", "D Major", "E Major", "F Major", "G Major",
        ]
        for i in range(10):
            self.assertIn(chord, allowed_values)
            time.sleep(1)
            next_chord = display.text
            self.assertNotEqual(chord, next_chord)
            chord = next_chord

        # They stop
        stop = self.browser.find_elemenst_by_tag_name[1]("button")
        stop.click()
        self.assertEqual(display.text, "")
