import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from piano import views
from piano.models import PracticeSession

class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="person", password="secret")
        self.client.login(username="person", password="secret")



class PianoPageViewTests(ViewTest):

    def test_piano_page_view_uses_piano_page_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")



class PracticePageViewTests(ViewTest):

    def test_piano_practice_page_view_uses_piano_practice_page_template(self):
        response = self.client.get("/piano/practice/")
        self.assertTemplateUsed(response, "pianopractice.html")



class UpdatePageViewTests(ViewTest):

    def test_piano_update_page_view_uses_piano_update_page_template(self):
        response = self.client.get("/piano/update/")
        self.assertTemplateUsed(response, "pianoupdate.html")


    def test_piano_update_page_view_can_save_session(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        self.client.post("/piano/update/", {
         "date": "2010-01-03",
         "minutes": 45
        })
        self.assertEqual(PracticeSession.objects.count(), 1)
        session = PracticeSession.objects.first()
        self.assertEqual(session.minutes, 45)
        self.assertEqual(session.date, datetime.datetime(2010, 1, 3).date())


    def test_piano_update_page_view_redirects_after_POST(self):
        response = self.client.post("/piano/update/", {
         "date": "2010-01-03",
         "minutes": 45
        })
        self.assertRedirects(response, "/piano/update/")


    def test_piano_update_page_view_returns_error_message_when_needed(self):
        response = self.client.post("/piano/update/", {
         "date": "2010-01-03",
         "minutes": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot submit")


    def test_piano_update_page_view_does_not_save_to_db_after_error(self):
        self.assertEqual(PracticeSession.objects.count(), 0)
        response = self.client.post("/piano/update/", {
         "date": "2010-01-03",
         "minutes": ""
        })
        self.assertEqual(PracticeSession.objects.count(), 0)
