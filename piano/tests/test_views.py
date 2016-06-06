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

    def test_piano_update_page_view_is_protected(self):
        self.client.logout()
        response = self.client.get("/piano/update/")
        self.assertRedirects(response, "/")


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


    def test_piano_update_page_view_shows_all_sessions_in_correct_order(self):
        PracticeSession.objects.create(
         date=datetime.datetime(1991, 9, 28).date(),
         minutes=10
        )
        PracticeSession.objects.create(
         date=datetime.datetime(1992, 9, 28).date(),
         minutes=10
        )
        PracticeSession.objects.create(
         date=datetime.datetime(1990, 9, 28).date(),
         minutes=10
        )
        response = self.client.get("/piano/update/")
        pos_1990 = response.content.decode().find("September, 1990")
        pos_1991 = response.content.decode().find("September, 1991")
        pos_1992 = response.content.decode().find("September, 1992")
        self.assertTrue(pos_1992 < pos_1991 < pos_1990)



class DeletePageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        PracticeSession.objects.create(minutes=10, date=datetime.datetime.now())

    def test_piano_delete_page_view_is_protected(self):
        self.client.logout()
        response = self.client.get("/piano/delete/1/")
        self.assertRedirects(response, "/")


    def test_piano_delete_page_view_uses_piano_delete_page_template(self):
        response = self.client.get("/piano/delete/1/")
        self.assertTemplateUsed(response, "pianodelete.html")


    def test_piano_update_page_view_redirects_after_POST(self):
        response = self.client.post("/piano/delete/1/")
        self.assertRedirects(response, "/piano/update/")


    def test_piano_update_page_view_can_delete_sessions(self):
        self.assertEqual(PracticeSession.objects.count(), 1)
        response = self.client.post("/piano/delete/1/")
        self.assertEqual(PracticeSession.objects.count(), 0)
