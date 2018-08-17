from selenium import webdriver
from testarsenal import BrowserTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase, BrowserTest):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.close()
