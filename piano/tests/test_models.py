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
