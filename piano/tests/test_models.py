from datetime import datetime
from django.core.exceptions import ValidationError
from samireland.tests import ModelTest
from piano.models import PracticeSession

class PracticeSessionTest(ModelTest):

    def test_save_and_retrieve_practice_sessions(self):
        self.assertEqual(PracticeSession.objects.all().count(), 0)
        session = PracticeSession()
        session.minutes = 25
        session.date = datetime(1939, 9, 1).date()
        session.save()
        self.assertEqual(PracticeSession.objects.all().count(), 1)

        retrieved_session = PracticeSession.objects.first()
        self.assertEqual(retrieved_session, session)


    def test_practice_session_date_has_to_be_unique(self):
        today = datetime.now().date()
        PracticeSession.objects.create(minutes=5, date=today)
        with self.assertRaises(ValidationError):
            post = PracticeSession(minutes=10, date=today)
            post.full_clean()



class CumulativePracticeTests(ModelTest):

    def test_can_get_cumulative_practice_time(self):
        s1 = PracticeSession.objects.create(minutes=5, date=datetime(2011, 1, 1))
        self.assertEqual(s1.cumulative_minutes, 5)
        s2 = PracticeSession.objects.create(minutes=15, date=datetime(2011, 1, 2))
        self.assertEqual(s1.cumulative_minutes, 5)
        self.assertEqual(s2.cumulative_minutes, 20)
        s3 = PracticeSession.objects.create(minutes=20, date=datetime(2011, 1, 3))
        self.assertEqual(s1.cumulative_minutes, 5)
        self.assertEqual(s2.cumulative_minutes, 20)
        self.assertEqual(s3.cumulative_minutes, 40)
        s4 = PracticeSession.objects.create(minutes=5, date=datetime(2011, 1, 8))
        self.assertEqual(s1.cumulative_minutes, 5)
        self.assertEqual(s2.cumulative_minutes, 20)
        self.assertEqual(s3.cumulative_minutes, 40)
        self.assertEqual(s4.cumulative_minutes, 45)
