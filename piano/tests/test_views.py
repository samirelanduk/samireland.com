from datetime import datetime, timedelta
from random import randint
from unittest.mock import patch
from home.models import EditableText
from piano.models import PracticeSession
from piano.views import today, get_practice_time
from piano.views import get_last_sixty, get_last_sixty_cumulative
from piano.views import get_last_year, get_last_year_cumulative
from piano.views import get_all, get_all_cumulative
from samireland.tests import ViewTest

class TodayFunctionTests(ViewTest):

    def test_can_today_as_date(self):
        self.assertEqual(today(), datetime.now().date())



class PracticeTimeStringTests(ViewTest):

    def test_0_hour_string(self):
        self.assertEqual(get_practice_time(), "0 hours")


    def test_10_minutes_string(self):
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=10)
        self.assertEqual(get_practice_time(), "10 minutes")


    def test_1_hour_string(self):
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=60)
        self.assertEqual(get_practice_time(), "1 hour")


    def test_1_hour_10_minutes_string(self):
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=70)
        self.assertEqual(get_practice_time(), "1 hour and 10 minutes")


    def test_2_hours_string(self):
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=120)
        self.assertEqual(get_practice_time(), "2 hours")


    def test_2_hours_10_minutes_string(self):
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=130)
        self.assertEqual(get_practice_time(), "2 hours and 10 minutes")



class LastSixtyFunctionTests(ViewTest):

    def test_empty_series_when_no_sessions(self):
        self.assertEqual(get_last_sixty(), [])


    @patch("piano.views.today")
    def test_can_get_sessions_in_last_sixty_days(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2016, 5, 3), minutes=130)
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=10)
        PracticeSession.objects.create(date=datetime(2016, 7, 1), minutes=20)
        self.assertEqual(get_last_sixty(), [
         [1462233600000, 130], [1462665600000, 10], [1467331200000, 20]
        ])


    @patch("piano.views.today")
    def test_can_get_exclude_sessions_before_sixty_days(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2016, 5, 2), minutes=130)
        PracticeSession.objects.create(date=datetime(2016, 5, 3), minutes=130)
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=10)
        PracticeSession.objects.create(date=datetime(2016, 7, 1), minutes=20)
        PracticeSession.objects.create(date=datetime(2016, 7, 2), minutes=20)
        self.assertEqual(get_last_sixty(), [
         [1462233600000, 130], [1462665600000, 10], [1467331200000, 20]
        ])



class LastSixtyCumulativeTestsFunctionTests(ViewTest):

    @patch("piano.views.today")
    def test_no_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        data = get_last_sixty_cumulative()
        self.assertEqual(len(data), 60)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1462233600000 + (86400000 * i) for i in range(60)])
        self.assertEqual(minutes, [0 for i in range(60)])


    @patch("piano.views.today")
    def test_contained_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 6, 29), minutes=30)
        data = get_last_sixty_cumulative()
        self.assertEqual(len(data), 60)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1462233600000 + (86400000 * i) for i in range(60)])
        self.assertEqual(minutes, [0] * 5 + [0.25] * 52 + [0.75] * 3)


    @patch("piano.views.today")
    def test_all_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2016, 5, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 6, 29), minutes=30)
        data = get_last_sixty_cumulative()
        self.assertEqual(len(data), 60)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1462233600000 + (86400000 * i) for i in range(60)])
        self.assertEqual(minutes, [2] * 5 + [2.25] * 52 + [2.75] * 3)



class LastYearFunctionTests(ViewTest):

    def test_empty_series_when_no_sessions(self):
        self.assertEqual(get_last_year(), [])


    @patch("piano.views.today")
    def test_can_get_sessions_in_last_365_days(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2015, 7, 3), minutes=130)
        PracticeSession.objects.create(date=datetime(2015, 8, 8), minutes=10)
        PracticeSession.objects.create(date=datetime(2016, 7, 1), minutes=20)
        self.assertEqual(get_last_year(), [
         [1435881600000, 130], [1438992000000, 10], [1467331200000, 20]
        ])


    @patch("piano.views.today")
    def test_can_get_exclude_sessions_before_365_days(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2015, 7, 2), minutes=130)
        PracticeSession.objects.create(date=datetime(2015, 7, 3), minutes=130)
        PracticeSession.objects.create(date=datetime(2015, 8, 8), minutes=10)
        PracticeSession.objects.create(date=datetime(2016, 7, 1), minutes=20)
        PracticeSession.objects.create(date=datetime(2016, 7, 2), minutes=20)
        self.assertEqual(get_last_year(), [
         [1435881600000, 130], [1438992000000, 10], [1467331200000, 20]
        ])



class LastYearCumulativeTestsFunctionTests(ViewTest):

    @patch("piano.views.today")
    def test_no_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        data = get_last_year_cumulative()
        self.assertEqual(len(data), 365)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1435881600000 + (86400000 * i) for i in range(365)])
        self.assertEqual(minutes, [0 for i in range(365)])


    @patch("piano.views.today")
    def test_contained_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2015, 7, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 6, 29), minutes=30)
        data = get_last_year_cumulative()
        self.assertEqual(len(data), 365)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1435881600000 + (86400000 * i) for i in range(365)])
        self.assertEqual(minutes, [0] * 5 + [0.25] * 357 + [0.75] * 3)


    @patch("piano.views.today")
    def test_all_sessions_cumulative(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        PracticeSession.objects.create(date=datetime(2016, 7, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2015, 7, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 6, 29), minutes=30)
        data = get_last_year_cumulative()
        self.assertEqual(len(data), 365)
        days = [d[0] for d in data]
        minutes = [d[1] for d in data]
        self.assertEqual(days, [1435881600000 + (86400000 * i) for i in range(365)])
        self.assertEqual(minutes, [0] * 5 + [0.25] * 357 + [0.75] * 3)



class AllSessionFunctionTests(ViewTest):

    def test_no_series_when_no_sessions(self):
        self.assertEqual(get_all(), [])


    @patch("piano.views.today")
    def test_all_sessions_series(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 15).date()
        PracticeSession.objects.create(date=datetime(2016, 4, 1), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 4, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2016, 5, 1), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 5, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 7, 10), minutes=30)
        self.assertEqual(get_all(), [
         [1459468800000, 135], [1462060800000, 150],
         [1464739200000, 0], [1467331200000, 30]
        ])



class AllSessionCumulativeFunctionTests(ViewTest):

    def test_no_series_when_no_sessions(self):
        self.assertEqual(get_all_cumulative(), [])


    @patch("piano.views.today")
    def test_all_sessions_series(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 15).date()
        PracticeSession.objects.create(date=datetime(2016, 4, 1), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 4, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2016, 5, 1), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 5, 2), minutes=120)
        PracticeSession.objects.create(date=datetime(2016, 5, 8), minutes=15)
        PracticeSession.objects.create(date=datetime(2016, 7, 10), minutes=30)
        self.assertEqual(get_all_cumulative(), [
         [1456790400000, 0], [1459468800000, 2.25], [1462060800000, 4.75],
         [1464739200000, 4.75], [1467331200000, 5.25]
        ])



class PianoPageViewTests(ViewTest):

    def test_piano_view_uses_piano_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")


    def test_piano_view_uses_piano_long_editable_text(self):
        EditableText.objects.create(name="piano-long", content="some content")
        response = self.client.get("/piano/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "piano-long")


    @patch("piano.views.get_practice_time")
    def test_piano_view_uses_practice_time_function(self, mock_practice_time):
        mock_practice_time.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["practice_time"], "teststring")


    @patch("piano.views.today")
    def test_piano_view_sends_correct_dates(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 1).date()
        response = self.client.get("/piano/")
        self.assertEqual(response.context["today"], 1467331200000)
        self.assertEqual(response.context["minus_60"], 1462233600000)
        self.assertEqual(response.context["minus_365"], 1435881600000)


    @patch("piano.views.today")
    def test_piano_view_sends_correct_months(self, mock_today):
        mock_today.return_value = datetime(2016, 7, 15).date()
        PracticeSession.objects.create(date=datetime(2015, 7, 8), minutes=15)
        response = self.client.get("/piano/")
        self.assertEqual(response.context["this_month"], 1467331200000)
        self.assertEqual(response.context["first_month"], 1435708800000)
        self.assertEqual(response.context["pre_month"], 1433116800000)


    @patch("piano.views.get_last_sixty")
    def test_piano_view_uses_function_for_last_sixty(self, mock_last_sixty):
        mock_last_sixty.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["last_sixty"], "teststring")


    @patch("piano.views.get_last_sixty_cumulative")
    def test_piano_view_uses_function_for_last_sixty(self, mock_last_sixty_cum):
        mock_last_sixty_cum.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["last_sixty_cumulative"], "teststring")


    @patch("piano.views.get_last_year")
    def test_piano_view_uses_function_for_last_sixty(self, mock_last_year):
        mock_last_year.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["last_year"], "teststring")


    @patch("piano.views.get_last_year_cumulative")
    def test_piano_view_uses_function_for_last_sixty(self, mock_last_year_cum):
        mock_last_year_cum.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["last_year_cumulative"], "teststring")


    @patch("piano.views.get_all")
    def test_piano_view_uses_function_for_all_sessions(self, mock_all):
        mock_all.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["all"], "teststring")


    @patch("piano.views.get_all_cumulative")
    def test_piano_view_uses_function_for_all_sessions_cumulative(self, mock_all_cum):
        mock_all_cum.return_value = "teststring"
        response = self.client.get("/piano/")
        self.assertEqual(response.context["all_cumulative"], "teststring")



class PianoUpdatePageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.client.login(username="testsam", password="testpassword")


    def test_piano_update_view_uses_piano_update_template(self):
        response = self.client.get("/piano/update/")
        self.assertTemplateUsed(response, "piano-update.html")


    def test_cannot_access_piano_update_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/piano/update/")
        self.assertRedirects(response, "/")


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
        self.client.login(username="testsam", password="testpassword")
        PracticeSession.objects.create(date=datetime(2017, 3, 1), minutes=10)


    def test_piano_delete_view_uses_piano_delete_template(self):
        response = self.client.get("/piano/delete/1/")
        self.assertTemplateUsed(response, "piano-delete.html")


    def test_cannot_access_piano_delete_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/piano/delete/1/")
        self.assertRedirects(response, "/")


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
