from samireland.tests import ViewTest

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")



class LoginViewTests(ViewTest):

    def test_login_view_uses_login_template(self):
        response = self.client.get("/authenticate/")
        self.assertTemplateUsed(response, "login.html")


    def test_login_view_redirects_to_home_on_post(self):
        response = self.client.post("/authenticate/", data={
         "username": "testsam",
         "password": "testpassword"
        })
        self.assertRedirects(response, "/")


    def test_login_view_can_login(self):
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post("/authenticate/", data={
         "username": "testsam",
         "password": "testpassword"
        })
        self.assertIn("_auth_user_id", self.client.session)
