import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class MusicContentTest(FunctionalTest):

    def test_main_music_page_looks_right(self):
        # The user goes to the music page
        self.browser.get(self.live_server_url + "/piano/")

        # 'Learning Piano' is in the header, and the title
        self.assertIn("Learning Piano", self.browser.title)
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertIn("Learning Piano", h1.text)

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
        self.browser.get(self.live_server_url + "/piano/")

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
         "Past Sixty Days"
        )
        charts = past_thirty.find_elements_by_class_name("chart")
        self.assertEqual(len(charts), 2)
        for chart in charts:
            self.assertIsNot(chart.find_element_by_tag_name("svg"), None)

        # There is a sub-section on the past year
        past_year = progress.find_element_by_id("year")
        self.assertEqual(
         past_year.find_element_by_tag_name("h3").text,
         "Past Twelve Months"
        )
        charts = past_year.find_elements_by_class_name("chart")
        self.assertEqual(len(charts), 2)
        for chart in charts:
            self.assertIsNot(chart.find_element_by_tag_name("svg"), None)



class PracticeAppTest(FunctionalTest):

    def test_can_practice_notes(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/piano/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The first option is notes - they click it
        self.assertEqual(
         options[0].get_attribute("value"),
         "Notes"
        )
        options[0].click()

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id("id_seconds")
        seconds.send_keys("0.1")

        # They start the practice
        start = self.browser.find_element_by_id("start")
        canvas = self.browser.find_element_by_tag_name("canvas")
        self.assertEqual(canvas.get_attribute("display"), "")
        start.click()

        # They go for ten seconds
        note = canvas.get_attribute("display")
        allowed_values = [
         "A", "B", "C", "D", "E", "F", "G"
        ]
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(0.1)
            next_note = canvas.get_attribute("display")
            self.assertNotEqual(note, next_note)
            note = next_note

        # It's too much - they try again at two seconds
        stop = self.browser.find_element_by_id("stop")
        stop.click()
        time.sleep(0.2)
        self.assertEqual(canvas.get_attribute("display"), "")
        seconds.clear()
        seconds.send_keys("0.2")
        start.click()
        note = canvas.get_attribute("display")
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(0.2)
            next_note = canvas.get_attribute("display")
            self.assertNotEqual(note, next_note)
            note = next_note
        stop.click()


        # Feeling more confident, they decide to include black keys
        self.browser.find_element_by_id("id_black").click()
        allowed_values = [
         "A", "B", "C", "D", "E", "F", "G",
         "A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"
        ]
        start.click()
        note = canvas.get_attribute("display")
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(0.2)
            next_note = canvas.get_attribute("display")
            self.assertNotEqual(note, next_note)
            note = next_note


    def test_can_practice_chords(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/piano/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The first option is notes - they click it
        self.assertEqual(
         options[1].get_attribute("value"),
         "Chords"
        )
        options[1].click()

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id("id_seconds")
        seconds.send_keys("0.1")

        # They start the practice
        start = self.browser.find_element_by_id("start")
        canvas = self.browser.find_element_by_tag_name("canvas")
        self.assertEqual(canvas.get_attribute("display"), "")
        start.click()

        # They go for ten seconds
        chord = canvas.get_attribute("display")
        allowed_values = [
         "A Major", "B Major", "C Major", "D Major", "E Major", "F Major", "G Major",
        ]
        for i in range(10):
            self.assertIn(chord, allowed_values)
            time.sleep(0.1)
            next_chord = canvas.get_attribute("display")
            self.assertNotEqual(chord, next_chord)
            chord = next_chord

        # They stop
        stop = self.browser.find_element_by_id("stop")
        stop.click()
        time.sleep(0.2)
        self.assertEqual(canvas.get_attribute("display"), "")

        # Feeling more confident, they decide to include black keys
        self.browser.find_element_by_id("id_black").click()
        allowed_values = [
         "A Major", "B Major", "C Major", "D Major", "E Major", "F Major", "G Major",
         "A♭ Major", "A♯ Major", "B♭ Major", "C♯ Major", "D♭ Major", "D♯ Major",
         "E♭ Major", "F♯ Major", "G♭ Major", "G♯ Major"
        ]
        start.click()
        chord = canvas.get_attribute("display")
        for i in range(10):
            self.assertIn(chord, allowed_values)
            time.sleep(0.1)
            next_chord = canvas.get_attribute("display")
            self.assertNotEqual(chord, next_chord)
            chord = next_chord


    def test_can_practice_reading_notes(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/piano/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The first option is notes - they click it and get a grand staff
        self.assertEqual(
         options[2].get_attribute("value"),
         "Sheet Notes"
        )
        canvas = self.browser.find_element_by_tag_name("canvas")
        self.assertEqual(canvas.get_attribute("staff"), "no")
        options[2].click()
        self.assertEqual(canvas.get_attribute("staff"), "yes")

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id("id_seconds")
        seconds.send_keys("0.1")

        # They start the practice
        start = self.browser.find_element_by_id("start")
        self.assertEqual(canvas.get_attribute("display"), "")
        start.click()

        # They go for ten seconds
        note = canvas.get_attribute("display")
        notes = ["A", "B", "C", "D", "E", "F", "G"]
        keys = [2, 3, 4, 5]
        allowed_values = ["%s,%i"% (note, key) for note in notes for key in keys]
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(0.1)
            next_note = canvas.get_attribute("display")
            self.assertNotEqual(note, next_note)
            note = next_note

        # They stop
        stop = self.browser.find_element_by_id("stop")
        stop.click()
        time.sleep(0.2)
        self.assertEqual(canvas.get_attribute("display"), "")

        # Feeling more confident, they decide to include black keys
        self.browser.find_element_by_id("id_black").click()
        notes = [
         "A", "B", "C", "D", "E", "F", "G",
         "A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"
        ]
        allowed_values = ["%s,%i"% (note, key) for note in notes for key in keys]
        start.click()
        note = canvas.get_attribute("display")
        for i in range(10):
            self.assertIn(note, allowed_values)
            time.sleep(0.1)
            next_note = canvas.get_attribute("display")
            self.assertNotEqual(note, next_note)
            note = next_note

        # They stop and get rid of the staff
        stop.click()
        options[0].click()
        self.assertEqual(canvas.get_attribute("staff"), "no")



class UpdateTest(FunctionalTest):

    def add_practice(self, date, minutes):
        # There is a form for adding a new session
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        self.assertEqual(date_input.get_attribute("type"), "date")
        self.assertEqual(
         date_input.get_attribute("value"),
         datetime.datetime.now().strftime("%Y-%m-%d")
        )
        minutes_input = form.find_elements_by_tag_name("input")[1]
        self.assertEqual(minutes_input.get_attribute("type"), "text")
        submit = form.find_elements_by_tag_name("input")[-1]

        # Sam adds x minutes for the date
        date_input.send_keys(date.strftime("%d%m%Y"))
        minutes_input.send_keys(str(minutes))
        submit.click()

        # He is still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/piano/update/"
        )


    def test_can_add_practice_data(self):
        # Sam goes to the practice page
        self.sam_logs_in()
        self.browser.get(self.live_server_url + "/piano/update/")

        # There is a table for practice data, currently empty
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 0)

        self.add_practice(datetime.datetime.now(), 10)

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

        # He adds three more times
        self.add_practice(
         datetime.datetime.now() - datetime.timedelta(days=2),
         40
        )
        self.add_practice(
         datetime.datetime.now() - datetime.timedelta(days=90),
         5
        )
        self.add_practice(
         datetime.datetime.now() - datetime.timedelta(days=1),
         30
        )

        # The data is in the table
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 4)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "10"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[1].text,
         "30"
        )
        self.assertEqual(
         rows[2].find_elements_by_tag_name("td")[1].text,
         "40"
        )
        self.assertEqual(
         rows[3].find_elements_by_tag_name("td")[1].text,
         "5"
        )

        # Each of the rows has a delete button
        for row in rows[::-1]:
            last_cell = self.browser.find_elements_by_tag_name("td")[-1]
            form = last_cell.find_element_by_tag_name("form")
            delete_button = form.find_element_by_tag_name("input")
            self.assertEqual(
             delete_button.get_attribute("value"),
             "Delete"
            )

        # Sam deletes one of the sessions
        delete_button.click()

        # There are now three rows
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[1].text,
         "30"
        )
