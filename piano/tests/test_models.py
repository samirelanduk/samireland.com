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
