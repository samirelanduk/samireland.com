from .base import FunctionalTest

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

        # There is a posts
        posts = self.browser.find_element_by_id("blog-posts")
        self.assertIn("no blog posts", posts.text)
        with self.assertRaises(self.NoElement):
            posts.find_element_by_tag_name("a")
