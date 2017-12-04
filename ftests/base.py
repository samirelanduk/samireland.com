from selenium import webdriver
from seleniumx import TestCaseX
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

class FunctionalTest(StaticLiveServerTestCase, TestCaseX):

    def setUp(self):
        self.browser = webdriver.Chrome()
        User.objects.create_user(
         username="testsam",
         password="testpassword"
        )


    def tearDown(self):
        self.browser.close()


    def login(self):
        self.client.login(username="testsam", password="testpassword")
        cookie = self.client.cookies["sessionid"].value
        self.browser.get(self.live_server_url + "/")
        self.browser.add_cookie({
         "name": "sessionid", "value": cookie, "secure": False, "path": "/"
        })
        self.browser.refresh()
