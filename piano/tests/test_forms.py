import datetime
from django.test import TestCase
from piano.forms import PracticeSessionForm
from piano.models import PracticeSession

class SessionFormsRenderingTest(TestCase):

    def test_session_form_has_correct_inputs(self):
        form = PracticeSessionForm()
        self.assertIn(
         'name="date" type="date"',
         str(form)
        )
        self.assertIn(
         'name="minutes" placeholder="Minutes" type="text"',
         str(form)
        )



class FormsValidationTest(TestCase):

    def test_blog_form_wont_accept_blank_minutes(self):
        form = PracticeSessionForm(data={
         "date": "1939-09-01",
         "minutes": ""
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["minutes"],
         ["You cannot submit a session with no minutes"]
        )
        form = PracticeSessionForm(data={
         "date": "1939-09-01",
         "minutes": "0"
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["minutes"],
         ["You cannot submit a session with no minutes"]
        )


    def test_blog_form_wont_accept_blank_date(self):
        form = PracticeSessionForm(data={
         "date": "",
         "minutes": "5",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["date"],
         ["You cannot submit a session with no date"]
        )


    def test_blog_form_wont_accept_duplicate_dates(self):
        date = datetime.datetime(1990, 9, 28).date()
        PracticeSession.objects.create(minutes="5", date=date)
        form = PracticeSessionForm(data={
         "title": "10",
         "date": "1990-09-28"
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["date"],
         ["There is already a session for this date"]
        )
