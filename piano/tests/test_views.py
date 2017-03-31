from datetime import datetime
from home.models import EditableText
from samireland.tests import ViewTest

class PianoPageViewTests(ViewTest):

    def test_piano_view_uses_piano_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")


    def test_piano_view_uses_piano_long_editable_text(self):
        EditableText.objects.create(name="piano-long", content="some content")
        response = self.client.get("/piano/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "piano-long")



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
