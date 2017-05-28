"""Contains tests for the blog section."""

from time import sleep
from datetime import datetime
from .base import FunctionalTest

class BlogCreationTests(FunctionalTest):

    def test_can_create_blog_post(self):
        self.login()
        self.get("/")

        # There is a blog link in the header
        header = self.browser.find_element_by_tag_name("header")
        blog_link = header.find_element_by_id("blog-link")

        # They click it and are taken to the blog creation page
        blog_link.click()
        self.check_page("/blog/new/")


    def test_blog_post_needs_correct_date(self):
        pass


    def test_blog_post_needs_correct_title(self):
        pass


    def test_blog_post_needs_correct_body(self):
        pass



class BlogReadingTests(FunctionalTest):

    def test_can_cycle_between_blog_posts(self):
        pass


    def test_can_get_blog_posts_by_period(self):
        pass



class BlogModificationTests(FunctionalTest):

    def test_can_modify_blog_post(self):
        pass


    def test_modified_blog_post_needs_correct_date(self):
        pass


    def test_modified_blog_post_needs_correct_title(self):
        pass


    def test_modified_blog_post_needs_correct_body(self):
        pass



class BlogDeletionTests(FunctionalTest):

    def test_can_delete_blog_post(self):
        pass



class BlogAccessTests(FunctionalTest):

    def test_cannot_access_new_blog_page_when_not_logged_in(self):
        pass


    def test_cannot_access_blog_edit_page_when_not_logged_in(self):
        pass


    def test_cannot_access_blog_delete_page_when_not_logged_in(self):
        pass
