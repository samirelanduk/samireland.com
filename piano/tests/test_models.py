import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from piano.models import PracticeSession

class PracticeSessionTest(TestCase):

    def test_save_and_retrieve_practice_sessions(self):
        self.assertEqual(PracticeSession.objects.all().count(), 0)
        session = PracticeSession()
        session.minutes = 25
        session.date = datetime.datetime(1939, 9, 1).date()
        session.save()
        self.assertEqual(PracticeSession.objects.all().count(), 1)

        retrieved_session = PracticeSession.objects.first()
        self.assertEqual(retrieved_session, session)



class PracticeSessionValidationTest(TestCase):

    def test_cannot_create_session_without_minutes(self):
        session = PracticeSession(date=datetime.datetime.now().date())
        with self.assertRaises(ValidationError):
            session.full_clean()
        session = PracticeSession(minutes=0, date=datetime.datetime.now().date())
        with self.assertRaises(ValidationError):
            session.full_clean()


    def test_cannot_create_post_without_date(self):
        session = PracticeSession(minutes=5)
        with self.assertRaises(ValidationError):
            session.full_clean()


    def test_cannot_create_two_posts_with_same_date(self):
        today = datetime.datetime.now().date()
        PracticeSession.objects.create(minutes=5, date=today)
        with self.assertRaises(ValidationError):
            post = PracticeSession(minutes=10, date=today)
            post.full_clean()
