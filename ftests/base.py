from selenium import webdriver
from django.test import TestCase

class FunctionalTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()
