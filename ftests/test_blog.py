from .base import FunctionalTest
from samireland.models import BlogPost

class BlogPageTests(FunctionalTest):

    def test_blog_page_layout(self):
        # The user goes to the blog page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[4])

        # The page has the correct heading
        self.check_page("/blog/")
        self.check_title("Blog")
        self.check_h1("Blog")

        # There is a posts section
        posts = self.browser.find_element_by_id("blog-posts")
        self.assertIn("no blog posts", posts.text)
        with self.assertRaises(self.NoElement):
            posts.find_element_by_tag_name("a")


    def test_blog_posts_order(self):
        BlogPost.objects.create(date="2017-01-01", title="T1", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-03", title="T2", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-02", title="T3", body="1\n\n2")

        # They go to the page and look at the posts - there are 3
        self.get("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        posts = posts.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 3)

        # They are in the correct order
        self.assertEqual(
         posts[0].find_element_by_tag_name("h2").text, "T2"
        )
        self.assertEqual(
         posts[1].find_element_by_tag_name("h2").text, "T3"
        )
        self.assertEqual(
         posts[2].find_element_by_tag_name("h2").text, "T1"
        )


    def test_blog_navigation(self):
        BlogPost.objects.create(date="2017-01-01", title="T1", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-03", title="T2", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-02", title="T3", body="1\n\n2")

        # The user goes to the blog page and none of the posts have navigations
        self.get("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        posts = posts.find_elements_by_class_name("blog-post")
        for post in posts:
            with self.assertRaises(self.NoElement):
                post.find_element_by_id("posts-nav")

        # They go to the most recent post
        self.click(posts[0].find_element_by_tag_name("a"))
        self.check_page("/blog/2017/1/3/")

        # There is a nav section with a link to the previous page
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        with self.assertRaises(self.NoElement):
            nav.find_element_by_class_name("next-page")
        self.assertIn("Previous", previous.text)
        self.click(previous)
        self.check_page("/blog/2017/1/2/")

        # This page has both links, and they can still go back
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        next_ = nav.find_element_by_class_name("next-page")
        self.assertIn("Next", next_.text)
        self.assertIn("Previous", previous.text)
        self.click(previous)
        self.check_page("/blog/2017/1/1/")

        # The last page has no previous, but they can follow the next links
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        next_ = nav.find_element_by_class_name("next-page")
        self.assertEqual(previous.text, "")
        self.assertIn("Next", next_.text)
        self.click(next_)
        self.check_page("/blog/2017/1/2/")
        nav = self.browser.find_element_by_id("posts-nav")
        next_ = nav.find_element_by_class_name("next-page")
        self.click(next_)
        self.check_page("/blog/2017/1/3/")
