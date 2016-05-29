import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class MusicContentTest(FunctionalTest):

    def test_main_music_page_looks_right(self):
        # The user goes to the music page
        self.browser.get(self.live_server_url + "/piano/")

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
        self.browser.get(self.live_server_url + "/piano/practice/")

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
        options[1].find_elements_by_tag_name("input").click()

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


    def test_can_practice_reading_notes(self):
        # The user goes to the practice page
        self.browser.get(self.live_server_url + "/music/practice/")

        # There is a an option to specify the kind of practice to do
        options = self.browser.find_element_by_id(
         "options").find_elements_by_class_name("option")

        # The third option is reading - they click it
        self.assertEqual(
         options[2].find_elements_by_tag_name("label").text,
         "Reading Music"
        )
        options[2].find_elements_by_tag_name("input").click()

        # There is also an option to specify the number of seconds
        seconds = self.browser.find_element_by_id(
         "seconds").find_elements_by_tag_name("input")
        seconds.send_keys("1")

        # They start the practice
        start = self.browser.find_element_by_tag_name("button")
        display = self.browser.find_element_by_id("display")
        self.assertEqual(display.text, "")
        start.click()

        # There is svg in the display
        svg = display.find_element_by_tag_name("svg")

        # The SVG has five evenly spaced lines
        lines = svg.find_elements_by_tag_name("line")
        self.assertEqual(len(lines), 5)
        line_positions = [line.get_attribute("y1") for line in lines]
        gap = line_positions[1] - line_positions[0]
        self.assertEqual(line_positions[2] - line_positions[1], gap)
        self.assertEqual(line_positions[3] - line_positions[2], gap)
        self.assertEqual(line_positions[4] - line_positions[3], gap)

        # They go for ten seconds
        position = svg.find_element_by_tag_name("ellipse").get_attribute("cy")
        allowed_values = line_positions + [pos + (gap/2) for pos in line_positions]
        allowed_values += [line_positions[-1] + ((gap/2) * x) for x in range(6)]
        allowed_values += [line_positions[0] - ((gap/2) * x) for x in range(6)]
        for i in range(10):
            self.assertIn(position, allowed_values)
            time.sleep(1)
            next_position = svg.find_element_by_tag_name("ellipse").get_attribute("cy")
            self.assertNotEqual(position, next_position)
            position = next_position

        # They stop
        stop = self.browser.find_elemenst_by_tag_name[1]("button")
        stop.click()
        self.assertEqual(display.text, "")



class UpdateTest(FunctionalTest):

    def add_practice(self, date, minutes):
        # There is a form for adding a new session
        form = self.browser.find_element_by_tag_name("form")
        date = form.find_elements_by_tag_name("input")[0]
        self.assertEqual(minutes.get_attribute("type"), "date")
        self.assertEqual(
         date.get_attribute("value"),
         datetime.datetime.now().strftime("%Y-%m-%d")
        )
        minutes = form.find_elements_by_tag_name("input")[1]
        self.assertEqual(minutes.get_attribute("type"), "text")
        submit = form.find_elements_by_tag_name("input")[-1]

        # Sam adds x minutes for the date
        date.send_keys(date.strftime("%d%m%Y"))
        minutes.send_keys(str(minutes))
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
         datetime.datetime.now().strftime("%d %m, %Y")
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
