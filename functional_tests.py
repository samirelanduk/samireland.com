from selenium import webdriver
import unittest

class BlogContentTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def test_home_page_is_correct(self):
        # The user goes to the home page
        self.browser.get("http://localhost:8000")

        # 'Sam Ireland' is in the header, and the title
        self.assertIn("Sam Ireland", self.browser.title)
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Sam Ireland", header.text)

        # The nav bar has links to this page, the blog, and the about page
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.assertEqual(len(nav_links), 3)
        self.assertEqual(nav_links[0].text, "Home")
        self.assertEqual(
         nav_links[0].get_attribute("href"),
         "http://localhost:8000/"
        )
        self.assertEqual(nav_links[1].text, "Blog")
        self.assertEqual(
         nav_links[1].get_attribute("href"),
         "http://localhost:8000/blog/"
        )
        self.assertEqual(nav_links[2].text, "About")
        self.assertEqual(
         nav_links[2].get_attribute("href"),
         "http://localhost:8000/about/"
        )

        # The main content contains a welcome message
        main = self.browser.find_element_by_tag_name("main")
        heading = main.find_element_by_tag_name("h1")
        self.assertEqual(
         heading.text,
         "Hello."
        )
        welcome = main.find_element_by_id("welcome")
        self.assertIn("welcome", welcome.text.lower())
        self.assertGreaterEqual(len(welcome.find_elements_by_tag_name("p")), 3)

        # The main content also has a blog post
        latest_news = main.find_element_by_id("latest_news")
        self.assertEqual(
         latest_news.find_element_by_tag_name("h2").text,
         "Latest News"
        )
        blog_post = latest_news.find_element_by_class_name("blog_post")
        more_posts = latest_news.find_element_by_id("more_posts")
        self.assertEqual(more_posts.text, "More posts")
        self.assertEqual(
         more_posts.find_element_by_tag_name("a").get_attribute("href"),
         "http://localhost:8000/blog/"
        )

        # The footer contains image links to social profiles
        footer = self.browser.find_element_by_tag_name("footer")
        external_links = footer.find_element_by_id("external_links")
        external_links = external_links.find_elements_by_class_name("external_link")
        self.assertEqual(len(external_links), 7)
        required_links = [
         "http://facebok.com/samirelanduk/",
         "http://twitter.com/sam_m_ireland/",
         "http://linkedin.com/in/sam-ireland-42b73568/",
         "http://githib.com/samirelanduk/",
         "http://instagram.com/samirelanduk/",
         "http://youtube.com/channel/UCeitnG6LfY-F4C3jxHd-rRA/",
         "http://plus.google.com/+samireland/"
        ]
        for link in external_links:
            a = link.find_element_by_tag_name("a")
            img = a.find_element_by_tag_name("img")
            self.assertIn(a.get_attribute("href"), required_links)


    def test_about_page_is_correct(self):
        # The user goes to the about page
        self.browser.get("http://localhost:8000/about")

        # There is some descriptive information
        self.assertIn("About", self.browser.title)
        main = self.browser.find_element_by_tag_name("main")
        heading = main.find_element_by_tag_name("h1")
        self.assertEqual(heading.text.lower(), "about me")
        paragraphs = main.find_elements_by_tag_name("p")
        self.assertGreaterEqual(len(paragraphs), 5)




if __name__ == "__main__":
    unittest.main(warnings="ignore")
