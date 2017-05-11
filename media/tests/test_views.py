from samireland.tests import ViewTest

class MediaPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.client.login(username="testsam", password="testpassword")

    def test_piano_view_uses_piano_template(self):
        response = self.client.get("/media/")
        self.assertTemplateUsed(response, "media.html")


    def test_cannot_access_media_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/media/")
        self.assertRedirects(response, "/")
