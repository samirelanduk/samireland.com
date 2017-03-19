from home.models import EditableText
from samireland.tests import ViewTest

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


    def test_home_view_uses_home_editable_text(self):
        EditableText.objects.create(name="home", content="some content")
        response = self.client.get("/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "home")



class AboutPageViewTests(ViewTest):

    def test_about_view_uses_about_template(self):
        response = self.client.get("/about/")
        self.assertTemplateUsed(response, "about.html")


    def test_about_view_uses_home_editable_text(self):
        EditableText.objects.create(name="about", content="some content")
        response = self.client.get("/about/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "about")



class ResearchPageViewTests(ViewTest):

    def test_research_view_uses_research_template(self):
        response = self.client.get("/research/")
        self.assertTemplateUsed(response, "research.html")


    def test_about_view_uses_home_editable_text(self):
        EditableText.objects.create(name="research", content="some content")
        response = self.client.get("/research/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "research")



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

    def setUp(self):
        ViewTest.setUp(self)
        self.client.login(username="testsam", password="testpassword")


    def test_edit_view_uses_edit_template(self):
        response = self.client.get("/edit/home/")
        self.assertTemplateUsed(response, "edit.html")


    def test_edit_view_denies_entry_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/edit/home/")
        self.assertRedirects(response, "/")


    def test_edit_home_view_redirects_to_home_on_post(self):
        response = self.client.post("/edit/home/", data={"content": "some content"})
        self.assertRedirects(response, "/")


    def test_edit_about_view_redirects_to_about_on_post(self):
        response = self.client.post("/edit/about/", data={"content": "some content"})
        self.assertRedirects(response, "/about/")


    def test_edit_research_view_redirects_to_research_on_post(self):
        response = self.client.post("/edit/research/", data={"content": "some content"})
        self.assertRedirects(response, "/research/")


    def test_edit_view_can_create_home_text_record_if_it_doesnt_exist(self):
        self.assertEqual(len(EditableText.objects.filter(name="home")), 0)
        self.client.post("/edit/home/", data={"content": "some content"})
        self.assertEqual(len(EditableText.objects.filter(name="home")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "home")
        self.assertEqual(text.content, "some content")


    def test_edit_view_can_create_about_text_record_if_it_doesnt_exist(self):
        self.assertEqual(len(EditableText.objects.filter(name="about")), 0)
        self.client.post("/edit/about/", data={"content": "some content"})
        self.assertEqual(len(EditableText.objects.filter(name="about")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "about")
        self.assertEqual(text.content, "some content")


    def test_edit_view_can_create_research_text_record_if_it_doesnt_exist(self):
        self.assertEqual(len(EditableText.objects.filter(name="research")), 0)
        self.client.post("/edit/research/", data={"content": "some content"})
        self.assertEqual(len(EditableText.objects.filter(name="research")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "research")
        self.assertEqual(text.content, "some content")


    def test_edit_view_can_update_existing_home_text_record(self):
        EditableText.objects.create(name="home", content="some content")
        self.client.post("/edit/home/", data={"content": "new content"})
        self.assertEqual(len(EditableText.objects.filter(name="home")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "home")
        self.assertEqual(text.content, "new content")


    def test_edit_view_can_update_existing_about_text_record(self):
        EditableText.objects.create(name="about", content="some content")
        self.client.post("/edit/about/", data={"content": "new content"})
        self.assertEqual(len(EditableText.objects.filter(name="about")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "about")
        self.assertEqual(text.content, "new content")


    def test_edit_view_can_update_existing_research_text_record(self):
        EditableText.objects.create(name="research", content="some content")
        self.client.post("/edit/research/", data={"content": "new content"})
        self.assertEqual(len(EditableText.objects.filter(name="research")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "research")
        self.assertEqual(text.content, "new content")


    def test_only_certain_names_can_be_edited(self):
        response = self.client.get("/edit/wrongwrongwrong/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/edit/home/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/edit/about/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/edit/research/")
        self.assertEqual(response.status_code, 200)


    def test_edit_view_uses_home_text_in_form(self):
        EditableText.objects.create(name="home", content="some content")
        response = self.client.get("/edit/home/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "home")
        self.assertContains(response, "some content</textarea>")


    def test_edit_view_uses_about_text_in_form(self):
        EditableText.objects.create(name="about", content="some content")
        response = self.client.get("/edit/about/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "about")
        self.assertContains(response, "some content</textarea>")


    def test_edit_view_uses_research_text_in_form(self):
        EditableText.objects.create(name="research", content="some content")
        response = self.client.get("/edit/research/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "research")
        self.assertContains(response, "some content</textarea>")
