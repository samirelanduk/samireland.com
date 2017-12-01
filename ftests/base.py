from selenium import webdriver
from seleniumx import TestCaseX
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase, TestCaseX):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.close()
