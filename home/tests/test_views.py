from datetime import datetime
from home.models import EditableText, Publication
from blog.models import BlogPost
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


    def test_home_view_sends_most_recent_visible_post(self):
        BlogPost.objects.create(
         date="1990-09-2", title="t", body="b1", visible=True
        )
        BlogPost.objects.create(
         date="1990-09-1", title="t", body="b2", visible=True
        )
        BlogPost.objects.create(
         date="1990-09-3", title="t", body="b3", visible=False
        )
        response = self.client.get("/")
        self.assertEqual(response.context["post"].body, "b1")



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


    def test_research_page_sends_all_publications(self):
        p1 = Publication.objects.create(
         pk="publication-1", title="Title1", date=datetime(2014, 1, 6).date(),
         url="http://cat.com", doi="d.1", authors="Bob, Joe",
         abstract="Line 1\n\nLine 2", body="L1\nL2\nL3"
        )
        p2 = Publication.objects.create(
         pk="publication-2", title="Title2", date=datetime(2015, 1, 6).date(),
         url="http://dog.com", doi="d.5", authors="Bob, Joe2",
         abstract="Line1\n\nLine2", body="L1\nL2\nL3\nL4"
        )
        p3 = Publication.objects.create(
         pk="publication-3", title="Title3", date=datetime(2011, 1, 6).date(),
         url="http://fox.com", doi="d.2", authors="Bob, Joe, **Frank**",
         abstract="Line A\n\nLine B", body="L11\nL21\nL31"
        )
        response = self.client.get("/research/")
        self.assertEqual(response.context["publications"][0], p2)
        self.assertEqual(response.context["publications"][1], p1)
        self.assertEqual(response.context["publications"][2], p3)



class NewResearchPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.data = {
         "id": "page-id-2", "title": "TITLE", "date": "2014-06-01",
         "url": "bob.com", "doi": "xxyyd-", "authors": "p1, p2",
         "abstract": "AAAA", "body": "BBBBBBBBB"
        }


    def test_new_research_view_uses_new_research_template(self):
        response = self.client.get("/research/new/")
        self.assertTemplateUsed(response, "new-publication.html")


    def test_new_research_view_denies_entry_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get("/research/new/")
        self.assertRedirects(response, "/")


    def test_new_research_view_redirects_on_post(self):
        response = self.client.post("/research/new/", data=self.data)
        self.assertRedirects(response, "/research/page-id-2/")


    def test_can_create_publication_on_post(self):
        self.assertEqual(Publication.objects.all().count(), 0)
        self.client.post("/research/new/", data=self.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        pub = Publication.objects.first()
        self.assertEqual(pub.id, "page-id-2")
        self.assertEqual(pub.title, "TITLE")
        self.assertEqual(pub.date, datetime(2014, 6, 1).date())
        self.assertEqual(pub.url, "bob.com")
        self.assertEqual(pub.doi, "xxyyd-")
        self.assertEqual(pub.authors, "p1, p2")
        self.assertEqual(pub.abstract, "AAAA")
        self.assertEqual(pub.body, "BBBBBBBBB")


    def test_publication_id_needed(self):
        self.data["id"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no id", response.context["error"].lower())


    def test_publication_id_must_be_valid(self):
        self.data["id"] = "hhhh^"
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("^", response.context["error"].lower())


    def test_publication_id_must_be_unique(self):
        Publication.objects.create(
         pk="page-id-2", title="T", date=datetime.now().date(),
         url="U", doi="d", authors="a", abstract="A", body="B"
        )
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("already", response.context["error"].lower())


    def test_publication_title_needed(self):
        self.data["title"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no title", response.context["error"].lower())


    def test_publication_date_needed(self):
        self.data["date"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no date", response.context["error"].lower())


    def test_publication_url_needed(self):
        self.data["url"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no url", response.context["error"].lower())


    def test_publication_doi_needed(self):
        self.data["doi"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no doi", response.context["error"].lower())


    def test_publication_authors_needed(self):
        self.data["authors"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no authors", response.context["error"].lower())


    def test_publication_abstract_needed(self):
        self.data["abstract"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no abstract", response.context["error"].lower())


    def test_publication_body_needed(self):
        self.data["body"] = ""
        response = self.client.post("/research/new/", data=self.data)
        self.assertTemplateUsed(response, "new-publication.html")
        self.assertIn("no body", response.context["error"].lower())



class PublicationPageViewTests(ViewTest):

    def setUp(self):
        Publication.objects.create(
         pk="pub-description-here", title="T", date=datetime.now().date(),
         url="U", doi="d", authors="a", abstract="A", body="B"
        )


    def test_publication_view_uses_publication_template(self):
        response = self.client.get("/research/pub-description-here/")
        self.assertTemplateUsed(response, "publication.html")


    def test_publication_view_sends_publication(self):
        response = self.client.get("/research/pub-description-here/")
        self.assertEqual(response.context["publication"], Publication.objects.first())


    def test_publication_view_can_send_404(self):
        response = self.client.get("/research/-here/")
        self.assertEqual(response.status_code, 404)



class EditResearchPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        Publication.objects.create(
         pk="pub-description-here", title="T", date=datetime.now().date(),
         url="U", doi="d", authors="a", abstract="A", body="B"
        )
        self.data = {
         "title": "TITLE", "date": "2014-06-01",
         "url": "bob.com", "doi": "xxyyd-", "authors": "p1, p2",
         "abstract": "AAAA", "body": "BBBBBBBBB"
        }


    def test_edit_research_view_uses_edit_research_template(self):
        response = self.client.get("/research/pub-description-here/edit/")
        self.assertTemplateUsed(response, "edit-publication.html")



class ProjectPageViewTests(ViewTest):

    def test_project_view_uses_project_template(self):
        response = self.client.get("/projects/")
        self.assertTemplateUsed(response, "projects.html")


    def test_project_view_uses_project_editable_text(self):
        EditableText.objects.create(name="projects", content="some content")
        response = self.client.get("/projects/")
        editable_text = response.context["projects_text"]
        self.assertEqual(editable_text.name, "projects")



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
        self.client.logout()
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


    def test_edit_projects_view_redirects_to_projects_on_post(self):
        response = self.client.post("/edit/projects/", data={"content": "some content"})
        self.assertRedirects(response, "/projects/")


    def test_edit_view_can_create_home_text_record_if_it_doesnt_exist(self):
        self.assertEqual(len(EditableText.objects.filter(name="home")), 0)
        self.client.post("/edit/home/", data={"content": "some content"})
        self.assertEqual(len(EditableText.objects.filter(name="home")), 1)
        text = EditableText.objects.first()
        self.assertEqual(text.name, "home")
        self.assertEqual(text.content, "some content")


    def test_edit_view_can_update_existing_home_text_record(self):
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
        response = self.client.get("/edit/about/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/edit/research/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/edit/projects/")
        self.assertEqual(response.status_code, 200)


    def test_edit_view_uses_home_text_in_form(self):
        EditableText.objects.create(name="home", content="some content")
        response = self.client.get("/edit/home/")
        editable_text = response.context["text"]
        self.assertEqual(editable_text.name, "home")
        self.assertContains(response, "some content</textarea>")
