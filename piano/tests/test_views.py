from samireland.tests import ViewTest

class PianoPageViewTests(ViewTest):

    def test_piano_view_uses_piano_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")
