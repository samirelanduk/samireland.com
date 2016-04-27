from selenium import webdriver
import time
from .base import FunctionalTest

class MainCssTest(FunctionalTest):

    def test_main_css_applies(self):
        self.browser.get(self.server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         body.value_of_css_property("font-family"),
         "'Roboto Slab'"
        )


    def test_resize_above_1000px(self):
        self.browser.get(self.server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.browser.set_window_size(1100, 800)
        self.assertEqual(
         body.value_of_css_property("width"),
         "1024px"
        )
        self.browser.set_window_size(900, 800)
        self.assertEqual(
         body.value_of_css_property("width"),
         "900px"
        )



class BlogCss(FunctionalTest):

    def test_blog_css_applies(self):
        self.browser.get(self.server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        post = self.browser.find_element_by_class_name("blog_post")
        self.assertNotEqual(
         body.value_of_css_property("background-color"),
         post.value_of_css_property("background-color")
        )
