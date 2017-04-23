from datetime import datetime, timedelta
from random import randint
from home.models import EditableText
from piano.models import PracticeSession
from samireland.tests import ViewTest

class PianoPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        today = datetime.now().date()
        day = two_years_ago = today - timedelta(days=730)
        self.piano_data = []
        while day <= today:
            self.piano_data.append({
             "day": day,
             "minutes": 5
            })
            self.piano_data[-1]["cumulative"] = sum(d["minutes"] for d in self.piano_data)
            day += timedelta(days=1)
        for day in self.piano_data:
            if day["minutes"]:
                PracticeSession.objects.create(date=day["day"], minutes=day["minutes"])


    def test_piano_view_uses_piano_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")


    def test_piano_view_uses_piano_long_editable_text(self):
        EditableText.objects.create(name="piano-long", content="some content")
        response = self.client.get("/piano/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "piano-long")


    def test_piano_view_gives_total_practice_time(self):
        PracticeSession.objects.all().delete()
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "0 hours")
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=10)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "10 minutes")
        PracticeSession.objects.create(date=datetime(2017, 3, 2), minutes=50)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "1 hour")
        PracticeSession.objects.create(date=datetime(2017, 3, 3), minutes=10)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "1 hour and 10 minutes")
        PracticeSession.objects.create(date=datetime(2017, 3, 4), minutes=50)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "2 hours")
        PracticeSession.objects.create(date=datetime(2017, 3, 5), minutes=10)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "2 hours and 10 minutes")


    def test_piano_view_sends_right_days(self):
        response = self.client.get("/piano/")
        today = datetime.now().date()
        today_minus_59 = today - timedelta(days=59)
        today_minus_364 = today - timedelta(days=364)
        self.assertEqual(response.context["today"], int(today.strftime("%s")) * 1000)
        self.assertEqual(response.context["minus_59"], int(today_minus_59.strftime("%s")) * 1000)
        self.assertEqual(response.context["minus_364"], int(today_minus_364.strftime("%s")) * 1000)


    def test_piano_view_sends_last_sixty_minutes(self):
        response = self.client.get("/piano/")
        for point in response.context["last_sixty"]:
            self.assertEqual(point[1], 5)


    def test_piano_view_sends_last_sixty_minutes_cumulative(self):
        response = self.client.get("/piano/")
        self.assertEqual(len(response.context["last_sixty_cumulative"]), 60)
        for index, point in enumerate(response.context["last_sixty_cumulative"]):
            if index: self.assertEqual(point[1], response.context["last_sixty_cumulative"][index - 1][1] + 5)


    def test_piano_view_sends_last_365_minutes(self):
        response = self.client.get("/piano/")
        self.assertEqual(len(response.context["last_365"]), 365)
        for point in response.context["last_365"]:
            self.assertEqual(point[1], 5)


    def test_piano_view_sends_last_365_minutes_cumulative(self):
        response = self.client.get("/piano/")
        self.assertEqual(len(response.context["last_365_cumulative"]), 365)
        for index, point in enumerate(response.context["last_365_cumulative"]):
            if index: self.assertEqual(point[1], response.context["last_365_cumulative"][index - 1][1] + 5)



class PianoUpdatePageViewTests(ViewTest):

    def test_piano_update_view_uses_piano_update_template(self):
        response = self.client.get("/piano/update/")
        self.assertTemplateUsed(response, "piano-update.html")


    def test_piano_update_view_sends_current_date(self):
        response = self.client.get("/piano/update/")
        self.assertEqual(
         response.context["today"],
         datetime.now().strftime("%Y-%m-%d")
        )


    def test_piano_update_view_reloads_on_post(self):
        response = self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": 45
        })
        self.assertRedirects(response, "/piano/update/")


    def test_piano_update_view_can_make_new_practice_session(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": 45
        })
        self.assertEqual(PracticeSession.objects.count(), 1)
        session = PracticeSession.objects.first()
        self.assertEqual(session.minutes, 45)
        self.assertEqual(session.date, datetime(2010, 1, 3).date())


    def test_date_needs_to_be_proper_in_piano_update_view(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        response = self.client.post("/piano/update/", data={
         "date": "",
         "minutes": 45
        })
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.assertEqual(
         response.context["error_text"],
         "You cannot submit a session with no date"
        )


    def test_date_needs_to_be_unique_in_piano_update_view(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": 45
        })
        response = self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": 10
        })
        self.assertEqual(
         response.context["error_text"],
         "There is already a session for this date"
        )


    def test_minutes_needs_to_be_given_in_piano_update_view(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        response = self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": ""
        })
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.assertEqual(
         response.context["error_text"],
         "You cannot submit a session with no minutes"
        )


    def test_minutes_needs_to_be_proper_in_piano_update_view(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        response = self.client.post("/piano/update/", data={
         "date": "2010-01-03",
         "minutes": "uhiud"
        })
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.assertEqual(
         response.context["error_text"],
         "Minutes have to be a number"
        )


    def test_piano_update_view_sends_all_practice_sessions(self):
        response = self.client.get("/piano/update/")
        self.assertEqual(response.context["sessions"], [])
        d1 = PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=10)
        response = self.client.get("/piano/update/")
        self.assertEqual(response.context["sessions"], [d1])
        d2 = PracticeSession.objects.create(date=datetime(2017, 3, 2), minutes=5)
        response = self.client.get("/piano/update/")
        self.assertEqual(response.context["sessions"], [d2, d1])
        d3 = PracticeSession.objects.create(date=datetime(2017, 2, 28), minutes=1)
        response = self.client.get("/piano/update/")
        self.assertEqual(response.context["sessions"], [d2, d1, d3])


class PianoDeletePageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=10)


    def test_piano_delete_view_uses_piano_delete_template(self):
        response = self.client.get("/piano/delete/1/")
        self.assertTemplateUsed(response, "piano-delete.html")


    def test_piano_delete_view_knows_session(self):
        response = self.client.get("/piano/delete/1/")
        self.assertEqual(
         response.context["session"],
         PracticeSession.objects.first()
        )


    def test_piano_delete_view_redirects_to_update_page_on_post(self):
        response = self.client.post("/piano/delete/1/")
        self.assertRedirects(response, "/piano/update/")


    def test_piano_delete_view_can_delete_given_id(self):
        self.assertEqual(PracticeSession.objects.all().count(), 1)
        self.assertEqual(PracticeSession.objects.first().pk, 1)
        self.client.post("/piano/delete/1/")
        self.assertEqual(PracticeSession.objects.all().count(), 0)


    def test_piano_delete_view_does_nothing_when_given_wrong_id(self):
        self.assertEqual(PracticeSession.objects.all().count(), 1)
        self.assertEqual(PracticeSession.objects.first().pk, 1)
        response = self.client.post("/piano/delete/2/")
        self.assertEqual(PracticeSession.objects.all().count(), 1)
        self.assertRedirects(response, "/piano/")
