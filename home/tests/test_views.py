from home.models import EditableText
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


    def test_login_view_redirects_to_fence_on_incorrect_post(self):
        response = self.client.post("/authenticate/", data={
         "username": "testsam",
         "password": "wrongpassword"
        })
        self.assertRedirects(response, "/youshallnotpass/")



class FenceViewTests(ViewTest):

    def test_fence_view_uses_fence_template(self):
        response = self.client.get("/youshallnotpass/")
        self.assertTemplateUsed(response, "fence.html")



class LogoutViewTests(ViewTest):

    def test_logout_view_redirects_to_home(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/")


    def test_logout_view_will_logout(self):
        self.client.login(username="testsam", password="testpassword")
        self.assertIn("_auth_user_id", self.client.session)
        self.client.get("/logout/")
        self.assertNotIn("_auth_user_id", self.client.session)



class EditViewTests(ViewTest):

    def test_edit_view_uses_edit_template(self):
        response = self.client.get("/edit/home/")
        self.assertTemplateUsed(response, "edit.html")


    def test_edit_view_redirects_to_home_on_post(self):
        response = self.client.post("/edit/home/", data={"content": "some content"})
        self.assertRedirects(response, "/")


    def test_edit_view_can_create_text_record_if_it_doesnt_exist(self):
        self.assertEqual(len(EditableText.objects.filter(name="home")), 0)
        self.client.post("/edit/home/", data={"content": "some content"})
        self.assertEqual(len(EditableText.objects.filter(name="home")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "home")
        self.assertEqual(text.content, "some content")


    def test_edit_view_can_update_existing_text_record(self):
        EditableText.objects.create(name="home", content="some content")
        self.client.post("/edit/home/", data={"content": "new content"})
        self.assertEqual(len(EditableText.objects.filter(name="home")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "home")
        self.assertEqual(text.content, "new content")


    def test_only_certain_names_can_be_edited(self):
        response = self.client.get("/edit/wrongwrongwrong/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/edit/home/")
        self.assertEqual(response.status_code, 200)
