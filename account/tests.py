from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.contrib.auth.models import AnonymousUser, User
from account import views

class AuthTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
         username="person",
         password="secret"
        )
        self.anonymous_user = AnonymousUser()


class TestUrls(AuthTest):

    def test_login_url_resolves_to_login_view(self):
        resolver = resolve("/account/login/")
        self.assertEqual(resolver.func, views.login_page)


    def test_logout_url_resolves_to_login_view(self):
        resolver = resolve("/account/logout/")
        self.assertEqual(resolver.func, views.logout_page)


    def test_barrier_url_resolves_to_barrier_view(self):
        resolver = resolve("/account/youshallnotpass/")
        self.assertEqual(resolver.func, views.barrier_page)



class TestViews(AuthTest):

    def test_login_view_uses_login_template(self):
        response = self.client.get("/account/login/")
        self.assertTemplateUsed(response, "login.html")


    def test_login_view_redirects_after_post(self):
        response = self.client.post("/account/login/", data={
         "username": "person",
         "password": "secret"
        })
        self.assertRedirects(response, "/")


    def test_login_view_can_actually_login(self):
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post("/account/login/", data={
         "username": "person",
         "password": "secret"
        })
        self.assertIn("_auth_user_id", self.client.session)


    def test_login_view_sends_strangers_away(self):
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post("/account/login/", data={
         "username": "person",
         "password": "wrongpassword"
        })
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(response, "/account/youshallnotpass/")


    def test_logout_view_can_actually_logout(self):
        self.client.login(username="person", password="secret")
        self.assertIn("_auth_user_id", self.client.session)
        response = self.client.get("/account/logout/")
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertRedirects(response, "/")


    def test_barrier_view_uses_barrier_template(self):
        response = self.client.get("/account/youshallnotpass/")
        self.assertTemplateUsed(response, "barrier.html")
