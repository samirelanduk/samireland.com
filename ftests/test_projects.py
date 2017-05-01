"""Contains tests for the projects section."""

from time import sleep
from random import randint
import datetime
from .base import FunctionalTest
from piano.models import PracticeSession

class ProjectPageTests(FunctionalTest):

    def test_project_page_leads_to_piano_project(self):
        self.browser.set_window_size(800, 600)
        self.get("/")

        # The third nav link goes to the project page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[2].click()
        self.check_page("/projects/")

        # There is a h1 and a block of text
        main = self.browser.find_element_by_tag_name("main")
        h1 = main.find_element_by_tag_name("h1")
        projects_summary = main.find_element_by_id("projects-summary")

        # There is no edit link because they are not logged in
        links = projects_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links), 0)

        # There is a div devoted to the piano project
        piano_section = main.find_element_by_id("piano-project")
        h2 = piano_section.find_element_by_tag_name("h2")
        piano_summary = piano_section.find_element_by_id("piano-project-summary")
        more_piano_link = piano_section.find_elements_by_tag_name("a")[-1]

        # There is no edit link because they are not logged in
        links = piano_summary.find_elements_by_tag_name("a")
        self.assertEqual(len(links), 0)

        # They click the link for more information and are taken to piano page
        more_piano_link.click()
        self.check_page("/piano/")

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
        self.check_can_edit_text("/projects/", "piano-project-summary", "piano-brief")


    def test_cannot_access_project_edit_page_when_not_logged_in(self):
        self.get("/edit/projects/")
        self.check_page("/")


    def test_cannot_access_piano_brief_edit_page_when_not_logged_in(self):
        self.get("/edit/projects-brief/")
        self.check_page("/")



class PianoProjectTests(FunctionalTest):

    def test_can_change_piano_description_text(self):
        self.check_can_edit_text(
         "/piano/", "piano-description", "piano-long"
        )


    def test_cannot_access_piano_brief_edit_page_when_not_logged_in(self):
        self.get("/edit/projects-long/")
        self.check_page("/")


    def test_can_update_piano_progress(self):
        self.login()
        self.get("/")

        # There is a piano link in the header
        header = self.browser.find_element_by_tag_name("header")
        piano_update_link = header.find_element_by_id("piano-update-link")

        # They click it and are taken to the piano update page
        piano_update_link.click()
        self.check_page("/piano/update/")

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
        self.check_page("/piano/update/")

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
        self.get("/piano/")
        piano_progress = self.browser.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("10 minutes", first_p.text)

        # The user adds 50 minutes for ages ago
        self.get("/piano/update")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        date_input.send_keys("22092004")
        minutes_input.send_keys("50")
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
        self.get("/piano/")
        piano_progress = self.browser.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("1 hour", first_p.text)

        # The user adds 90 minutes for the far future
        self.get("/piano/update")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        date_input.send_keys("28092090")
        minutes_input.send_keys("90")
        submit.click()

        # The new entry is on the table
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)
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
        self.get("/piano/")
        piano_progress = self.browser.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("2 hours and 30 minutes", first_p.text)

        # Each of the rows has a delete button on the update page
        self.get("/piano/update/")
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
        description = form.find_element_by_id("delete-description")
        self.assertIn("22 September, 2004", description.text)
        self.assertIn("50 minutes", description.text)
        warning = form.find_element_by_id("delete-warning")
        self.assertIn(
         "are you sure?",
         warning.text.lower()
        )

        # There is a back to safety link, and a delete button
        back_to_safety = form.find_element_by_tag_name("a")
        delete_button = form.find_elements_by_tag_name("input")[-1]

        # He goes back to safety
        back_to_safety.click()
        self.check_page("/piano/update/")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)

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
        self.check_page("/piano/update/")

        # There are now two rows
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
        self.get("/piano/")
        piano_progress = self.browser.find_element_by_id("piano-progress")
        first_p = piano_progress.find_element_by_tag_name("p")
        self.assertIn("1 hour and 40 minutes", first_p.text)


    def test_cannot_access_piano_update_page_when_not_logged_in(self):
        self.get("/piano/update/")
        self.check_page("/")


    def test_cannot_access_piano_delete_page_when_not_logged_in(self):
        self.get("/piano/delete/1/")
        self.check_page("/")


    def test_cannot_post_session_with_no_date(self):
        self.login()

        # He tries to submit a session with no date
        self.get("/piano/update/")
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
        self.get("/piano/update/")
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

        # He tries to submit a session with nonsense minutes
        self.get("/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        minutes_input = form.find_elements_by_tag_name("input")[1]
        minutes_input.send_keys("string")
        submit = form.find_elements_by_tag_name("input")[-1]
        submit.click()

        # It doesn't work
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 0)

        # There is an error message
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(error.text, "Minutes have to be a number")


    def test_cannot_post_session_with_duplicate_date(self):
        self.login()

        # He submits a post for today
        self.get("/piano/update/")
        form = self.browser.find_element_by_tag_name("form")
        minutes_input = form.find_elements_by_tag_name("input")[1]
        submit = form.find_elements_by_tag_name("input")[-1]
        minutes_input.send_keys(10)
        submit.click()

        # He tries to submit a session with the same date
        self.get("/piano/update/")
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


    def test_piano_charts(self):
        # Add a bunch of piano data. This goes back two years - there is data on
        # every seventh day
        today = datetime.datetime.now().date()
        day = two_years_ago = today - datetime.timedelta(days=730)
        piano_data = []
        while day <= today:
            piano_data.append({
             "day": day,
             "minutes": randint(1, 15) * 5 if not day.day % 7
              and day < today - datetime.timedelta(days=5) else 0
            })
            piano_data[-1]["cumulative"] = sum(d["minutes"] for d in piano_data)
            day += datetime.timedelta(days=1)
        for day in piano_data:
            if day["minutes"]:
                PracticeSession.objects.create(date=day["day"], minutes=day["minutes"])

        # The user goes to the piano page
        self.browser.get(self.live_server_url + "/piano/")

        # There is a progress section with 60 day, one year, and all time divs
        progress_div = self.browser.find_element_by_id("piano-progress")
        sixty_div = progress_div.find_element_by_id("sixty-day-charts")
        year_div = progress_div.find_element_by_id("one-year-charts")
        all_time_div = progress_div.find_element_by_id("all-time-charts")

        # The sixty day div has a heading and two charts
        sixty_heading = sixty_div.find_element_by_tag_name("h3")
        sixty_chart = sixty_div.find_element_by_id("sixty-day-bar-chart")
        sixty_cumul_chart = sixty_div.find_element_by_id("sixty-day-line-chart")

        # The sixty day bar chart is correct
        sixty_days_ago = today - datetime.timedelta(days=60)
        last_sixty_days = [s for s in piano_data if s["day"] > sixty_days_ago]
        self.assertEqual(
         self.browser.execute_script("return sixty_bar.xAxis[0].min;"),
         int((sixty_days_ago + datetime.timedelta(days=1)).strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return sixty_bar.xAxis[0].max;"),
         int(today.strftime("%s")) * 1000
        )
        days_with_minutes = [day for day in last_sixty_days if day["minutes"]]
        for index, day in enumerate(days_with_minutes):
            self.assertEqual(
             self.browser.execute_script("return sixty_bar.series[0].data[%i].x;" % index),
             int(days_with_minutes[index]["day"].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return sixty_bar.series[0].data[%i].y;" % index),
             days_with_minutes[index]["minutes"]
            )

        # The sixty day line chart is correct
        self.assertEqual(
         self.browser.execute_script("return sixty_line.xAxis[0].min;"),
         int((sixty_days_ago + datetime.timedelta(days=1)).strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return sixty_line.xAxis[0].max;"),
         int(today.strftime("%s")) * 1000
        )
        for index, day in enumerate(last_sixty_days):
            self.assertEqual(
             self.browser.execute_script("return sixty_line.series[0].data[%i].x;" % index),
             int(last_sixty_days[index]["day"].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return sixty_line.series[0].data[%i].y;" % index),
             last_sixty_days[index]["cumulative"] / 60
            )

        # The year div has a heading and two charts
        year_heading = year_div.find_element_by_tag_name("h3")
        year_chart = year_div.find_element_by_id("one-year-bar-chart")
        year_cumul_chart = year_div.find_element_by_id("one-year-line-chart")

        # The year bar chart is correct
        year_ago = today - datetime.timedelta(days=365)
        last_365_days = [s for s in piano_data if s["day"] > year_ago]
        self.assertEqual(
         self.browser.execute_script("return year_bar.xAxis[0].min;"),
         int((year_ago + datetime.timedelta(days=1)).strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return year_bar.xAxis[0].max;"),
         int(today.strftime("%s")) * 1000
        )
        days_with_minutes = [day for day in last_365_days if day["minutes"]]
        for index, day in enumerate(days_with_minutes):
            self.assertEqual(
             self.browser.execute_script("return year_bar.series[0].data[%i].x;" % index),
             int(days_with_minutes[index]["day"].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return year_bar.series[0].data[%i].y;" % index),
             days_with_minutes[index]["minutes"]
            )

        # The year line chart is correct
        self.assertEqual(
         self.browser.execute_script("return year_line.xAxis[0].min;"),
         int((year_ago + datetime.timedelta(days=1)).strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return year_line.xAxis[0].max;"),
         int(today.strftime("%s")) * 1000
        )
        for index, day in enumerate(last_365_days):
            self.assertEqual(
             self.browser.execute_script("return year_line.series[0].data[%i].x;" % index),
             int(last_365_days[index]["day"].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return year_line.series[0].data[%i].y;" % index),
             last_365_days[index]["cumulative"] / 60
            )

        # The all time div has a heading and two charts
        all_time_heading = all_time_div.find_element_by_tag_name("h3")
        all_time_chart = all_time_div.find_element_by_id("all-time-bar-chart")
        all_time_cumul_chart = all_time_div.find_element_by_id("all-time-line-chart")

        # The all time bar chart is correct
        first_month = datetime.datetime(
         piano_data[0]["day"].year, piano_data[0]["day"].month, 1
        ).date()
        pre_month = datetime.datetime(
         piano_data[0]["day"].year if
          piano_data[0]["day"].month != 1 else piano_data[0]["day"].year - 1,
         piano_data[0]["day"].month - 1 if piano_data[0]["day"].month != 1 else 12,
         1
        ).date()
        this_month = datetime.datetime(today.year, today.month, 1).date()
        all_data = [[pre_month, 0, 0]]
        while all_data[-1][0] < this_month:
            next_month = datetime.datetime(
             all_data[-1][0].year if all_data[-1][0].month != 12 else all_data[-1][0].year + 1,
             all_data[-1][0].month + 1 if all_data[-1][0].month != 12 else 1,
             1
            ).date()
            minutes = sum([d["minutes"] for d in piano_data
             if d["day"].year == next_month.year and d["day"].month == next_month.month])
            cum_minutes = all_data[-1][2] + minutes
            all_data.append([next_month, minutes, cum_minutes])
        self.assertEqual(
         self.browser.execute_script("return all_bar.xAxis[0].min;"),
         int(first_month.strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return all_bar.xAxis[0].max;"),
         int(this_month.strftime("%s")) * 1000
        )
        for index, day in enumerate(all_data[1:], start=1):
            self.assertEqual(
             self.browser.execute_script("return all_bar.series[0].data[%i].x;" % (index - 1)),
             int(all_data[index][0].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return all_bar.series[0].data[%i].y;" % (index - 1)),
             all_data[index][1]
            )

        # The all time line chart is correct
        self.assertEqual(
         self.browser.execute_script("return all_line.xAxis[0].min;"),
         int(pre_month.strftime("%s")) * 1000
        )
        self.assertEqual(
         self.browser.execute_script("return all_line.xAxis[0].max;"),
         int(this_month.strftime("%s")) * 1000
        )
        for index, day in enumerate(all_data):
            self.assertEqual(
             self.browser.execute_script("return all_line.series[0].data[%i].x;" % index),
             int(all_data[index][0].strftime("%s")) * 1000
            )
            self.assertEqual(
             self.browser.execute_script("return all_line.series[0].data[%i].y;" % index),
             all_data[index][2] / 60
            )
