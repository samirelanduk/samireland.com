from unittest.mock import patch, Mock
from seleniumx import TestCaseX
from django.http import Http404
from django.test import TestCase
from samireland.models import EditableText
from samireland.views import *

class ViewTest(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("samireland.views.grab_editable_text")
        self.mock_grab = self.patcher1.start()
        self.mock_grab.return_value = "EDTEXT"


    def tearDown(self):
        self.patcher1.stop()



class HomeViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(home, request, "home.html")


    def test_home_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(home, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("home")



class ResearchViewTests(ViewTest):

    def test_research_view_uses_research_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(research, request, "research.html")


    def test_research_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(research, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("research")



class NewPublicationViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.PublicationForm")
        self.mock_form = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_new_pub_view_uses_new_pub_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(new_pub, request, "new-pub.html")


    def test_new_pub_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(new_pub, request, "/")


    def test_new_pub_sends_fresh_form(self):
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(new_pub, request, {"form": "FORM"})
        self.mock_form.assert_called_with()



class AboutViewTests(ViewTest):

    def test_about_view_uses_about_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(about, request, "about.html")


    def test_about_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(about, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("about")



class LoginViewTests(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("django.contrib.auth.authenticate")
        self.patcher2 = patch("django.contrib.auth.login")
        self.mock_auth = self.patcher1.start()
        self.mock_login = self.patcher2.start()
        self.mock_auth.return_value = "USER"


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()


    def test_login_view_uses_login_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(login, request, "login.html")


    def test_login_view_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        self.check_view_redirects(login, request, "/")


    def test_login_view_logs_in(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        login(request)
        self.mock_auth.assert_called_with(username="sam", password="pass")
        self.mock_login.assert_called_with(request, "USER")


    def test_login_view_sends_error_on_auth_failure(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        self.mock_auth.return_value = None
        login(request)
        self.mock_auth.assert_called_with(username="sam", password="pass")
        self.assertFalse(self.mock_login.called)
        self.check_view_uses_template(login, request, "login.html")



class LogoutViewTests(TestCase, TestCaseX):

    @patch("django.contrib.auth.logout")
    def test_logout_view_redirects_home(self, mock_logout):
        request = self.make_request("---")
        self.check_view_redirects(logout, request, "/")


    @patch("django.contrib.auth.logout")
    def test_logout_view_logs_out(self, mock_logout):
        request = self.make_request("---")
        logout(request)
        mock_logout.assert_called()



class EditViewTests(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("samireland.views.EditableText.objects.get")
        self.mock_get = self.patcher1.start()
        self.mock_text = Mock()
        self.mock_text.body = "---"
        self.mock_get.return_value = self.mock_text


    def tearDown(self):
        self.patcher1.stop()


    def test_edit_view_returns_404_with_get(self):
        request = self.make_request("---", loggedin=True)
        with self.assertRaises(Http404):
            edit(request, "home")


    def test_edit_view_returns_404_with_unauthorised_post(self):
        request = self.make_request("---", method="post")
        with self.assertRaises(Http404):
            edit(request, "home")


    def test_redirects_to_specified_url(self):
        request = self.make_request("---", method="post", data={
         "redirect": "/login/", "body": "..."
        }, loggedin=True)
        self.check_view_redirects(edit, request, "/login/", "home")


    def test_can_update_editable_text(self):
        request = self.make_request("---", method="post", data={
         "redirect": "/login/", "body": "..."
        }, loggedin=True)
        edit(request, "home")
        self.mock_get.assert_called_with(name="home")
        self.assertEqual(self.mock_text.body, "...")
        self.mock_text.save.assert_called()



class EditableTextGrabberTests(TestCase):

    def setUp(self):
        self.patcher1 = patch("samireland.views.EditableText.objects.create")
        self.patcher2 = patch("samireland.views.EditableText.objects.get")
        self.mock_create = self.patcher1.start()
        self.mock_get = self.patcher2.start()
        self.mock_create.return_value = "EDTEXT"
        self.mock_get.side_effect = EditableText.DoesNotExist


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()


    def test_grabber_can_create_and_return_text(self):
        text = grab_editable_text("xxx")
        self.assertEqual(text, "EDTEXT")
        self.mock_create.assert_called_with(name="xxx", body="")


    def test_home_view_can_obtain_and_send_text(self):
        self.mock_get.side_effect = ["EDTEXT"]
        text = grab_editable_text("xxx")
        self.assertEqual(text, "EDTEXT")
        self.assertFalse(self.mock_create.called)
        self.mock_get.assert_called_with(name="xxx")
