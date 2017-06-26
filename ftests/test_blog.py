"""Contains tests for the blog section."""

from time import sleep
from datetime import datetime
from .base import FunctionalTest

class BlogTest(FunctionalTest):

    def enter_blog_post(self, date, title, body, visible):
        # There is a form for submitting a blog post
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, "New Blog Post")
        form = self.browser.find_element_by_tag_name("form")
        date_input, title_input = form.find_elements_by_tag_name("input")[:2]
        body_input = form.find_element_by_tag_name("textarea")
        visible_input = form.find_elements_by_tag_name("input")[2]
        visible_label = form.find_element_by_tag_name("label")
        self.assertEqual(date_input.get_attribute("type"), "date")
        self.assertEqual(title_input.get_attribute("type"), "text")
        self.assertEqual(visible_input.get_attribute("type"), "checkbox")

        # The form has today's date and visibility is checked
        today = datetime.now()
        self.assertEqual(date_input.get_attribute("value"), today.strftime("%Y-%m-%d"))
        self.assertTrue(visible_input.is_selected())

        # They enter a blog post
        date_input.send_keys(date)
        if not date:
            self.browser.execute_script(
             "document.getElementById('date').setAttribute('value', '');"
            )
        title_input.send_keys(title)
        body_input.send_keys(body)
        if not visible: visible_label.click()

        # They submit the blog post
        submit = form.find_elements_by_tag_name("input")[-1]
        submit.click()


    def check_blog_post(self, post, date, title, body, visible):
        date_div = post.find_element_by_class_name("post-date")
        self.assertEqual(date_div.text, date)
        title_div = post.find_element_by_class_name("post-title")
        self.assertEqual(title_div.text, title)
        body_div = post.find_element_by_class_name("post-body")
        paragraphs = body_div.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), len(body))
        for para_div, para_text in zip(paragraphs, body):
            self.assertEqual(para_div.text, para_text)
        if visible:
            self.assertEqual(float(post.value_of_css_property("opacity")), 1)
        else:
            self.assertLess(float(post.value_of_css_property("opacity")), 1)



class BlogCreationTests(BlogTest):

    def test_can_create_blog_post(self):
        self.login()
        self.get("/")

        # There is a blog link in the header
        header = self.browser.find_element_by_tag_name("header")
        blog_link = header.find_element_by_id("blog-link")

        # They click it and are taken to the blog creation page
        blog_link.click()
        self.check_page("/blog/new/")

        # They enter a blog post
        self.enter_blog_post(
         "01-06-2014", "My first post", "This is my first post!\n\nIt's super.", True
        )

        # They are on the blog posts page
        self.check_page("/blog/")
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, "Blog Posts")
        posts_section = self.browser.find_element_by_id("posts")

        # There is one blog post there
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)

        # The post has the correct details
        self.check_blog_post(
         posts[0], "1 June, 2014", "My first post", ["This is my first post!", "It's super."], True
        )

        # They enter three more blog posts, one of which is not visible
        self.get("/blog/new/")
        self.enter_blog_post(
         "01-06-2015", "Second post", "Year later.", True
        )
        self.get("/blog/new/")
        self.enter_blog_post(
         "01-03-2015", "Third post", "Shy.", False
        )
        self.get("/blog/new/")
        self.enter_blog_post(
         "01-06-2012", "Ancient post", "Cool\n\nCool\n\nCool", True
        )

        # They are on the blog posts page
        self.check_page("/blog/")
        posts_section = self.browser.find_element_by_id("posts")

        # There are four blog posts there (invisible is there because logged in)
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 4)

        # Details are correct and in order
        self.check_blog_post(
         posts[0], "1 June, 2015", "Second post", ["Year later."], True
        )
        self.check_blog_post(
         posts[1], "1 March, 2015", "Third post", ["Shy."], False
        )
        self.check_blog_post(
         posts[2], "1 June, 2014", "My first post", ["This is my first post!", "It's super."], True
        )
        self.check_blog_post(
         posts[3], "1 June, 2012", "Ancient post", ["Cool", "Cool", "Cool"], True
        )


    def test_blog_post_needs_correct_date(self):
        self.login()
        self.get("/blog/new/")

        # The user leaves the date blank but submits everything else
        self.enter_blog_post(
         "", "Post!", "Year later.", True
        )

        # The user is still on the new blog page
        self.check_page("/blog/new/")

        # There is an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "You cannot submit a post with no date")

        # They try entering a post with the same date twice
        self.get("/blog/new/")
        self.enter_blog_post(
         "01-06-2015", "Second post", "Year later.", True
        )
        self.get("/blog/new/")
        self.enter_blog_post(
         "01-06-2015", "Second post", "Year later.", True
        )

        # The user is still on the new blog page
        self.check_page("/blog/new/")

        # There is an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "There is already a post with that date")


    def test_blog_post_needs_correct_title(self):
        self.login()
        self.get("/blog/new/")

        # The user leaves the title blank but submits everything else
        self.enter_blog_post(
         "01-06-2015", "", "Year later.", True
        )

        # The user is still on the new blog page
        self.check_page("/blog/new/")

        # There is an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "You cannot submit a post with no title")


    def test_blog_post_needs_correct_body(self):
        self.login()
        self.get("/blog/new/")

        # The user leaves the body blank but submits everything else
        self.enter_blog_post(
         "01-06-2015", "TTT", "", True
        )

        # The user is still on the new blog page
        self.check_page("/blog/new/")

        # There is an error message
        form = self.browser.find_element_by_tag_name("form")
        error = form.find_element_by_class_name("error")
        self.assertEqual(error.text, "You cannot submit a post with no body")



class BlogReadingTests(BlogTest):

    def setUp(self):
        BlogTest.setUp(self)


    def test_can_cycle_between_blog_posts(self):
        self.browser.set_window_size(800, 600)
        self.get("/")

        # The user clicks the blog link in the header
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[4].click()
        self.check_page("/blog/")


    def test_can_get_blog_posts_by_period(self):
        pass



class BlogModificationTests(BlogTest):

    def test_can_modify_blog_post(self):
        pass


    def test_modified_blog_post_needs_correct_date(self):
        pass


    def test_modified_blog_post_needs_correct_title(self):
        pass


    def test_modified_blog_post_needs_correct_body(self):
        pass



class BlogDeletionTests(BlogTest):

    def test_can_delete_blog_post(self):
        pass



class BlogAccessTests(BlogTest):

    def test_cannot_access_new_blog_page_when_not_logged_in(self):
        pass


    def test_cannot_access_blog_edit_page_when_not_logged_in(self):
        pass


    def test_cannot_access_blog_delete_page_when_not_logged_in(self):
        pass
