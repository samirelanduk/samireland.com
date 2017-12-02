from unittest.mock import patch, Mock
from seleniumx import TestCaseX
from django.http import Http404
from django.test import TestCase
from samireland.views import *

class HomeViewTests(TestCase, TestCaseX):

    def test_home_view_uses_home_template(self):
        request = self.get_request("---")
        self.check_view_uses_template(home, request, "home.html")



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
        request = self.get_request("---")
        self.check_view_uses_template(login, request, "login.html")


    def test_login_view_redirects_on_post(self):
        request = self.get_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        self.check_view_redirects(login, request, "/")


    def test_login_view_logs_in(self):
        request = self.get_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        login(request)
        self.mock_auth.assert_called_with(username="sam", password="pass")
        self.mock_login.assert_called_with(request, "USER")
