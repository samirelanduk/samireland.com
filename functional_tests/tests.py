from selenium import webdriver
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class BlogContentTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def test_home_page_is_correct(self):
        # The user goes to the home page
        self.browser.get(self.live_server_url)

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
         self.live_server_url + "/"
        )
        self.assertEqual(nav_links[1].text, "Blog")
        self.assertEqual(
         nav_links[1].get_attribute("href"),
         self.live_server_url + "/blog/"
        )
        self.assertEqual(nav_links[2].text, "About")
        self.assertEqual(
         nav_links[2].get_attribute("href"),
         self.live_server_url + "/about/"
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
         self.live_server_url + "/blog/"
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
        self.browser.get(self.live_server_url + "/about")

        # There is some descriptive information
        self.assertIn("About", self.browser.title)
        main = self.browser.find_element_by_tag_name("main")
        heading = main.find_element_by_tag_name("h1")
        self.assertEqual(heading.text.lower(), "about me")
        paragraphs = main.find_elements_by_tag_name("p")
        self.assertGreaterEqual(len(paragraphs), 5)



class BlogPostingTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()


    def tearDown(self):
        self.browser.quit()


    def sam_writes_blog_post(self, title, date, body, visible):
        # Sam goes to new post page
        self.browser.get(self.live_server_url + "/blog/new/")

        # There is a form for entering a blog post
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        date_entry = form.find_elements_by_tag_name("input")[1]
        body_entry = form.find_element_by_tag_name("textarea")
        live_box = form.find_elements_by_tag_name("input")[2]
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.assertEqual(title_entry.get_attribute("type"), "text")
        self.assertEqual(date_entry.get_attribute("type"), "date")
        self.assertEqual(live_box.get_attribute("type"), "checkbox")

        # Sam posts a blog post
        title_entry.send_keys(title)
        date_entry.send_keys(date)
        body_entry.send_keys(body)
        if (live_box.is_selected() and not visible) or (not live_box.is_selected() and visible):
            live_box.click()
        submit_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/"
        )


    def test_sam_can_post_blogs(self):
        # Sam posts a first blog post
        self.sam_writes_blog_post(
         "My first blog post",
         "10101962",
         "My first blog post!",
         True
        )

        # Sam goes away, another mighty victory achieved
        self.browser.quit()

        # One of Sam's many fans comes to the site
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)

        # There is the blog post
        blog_post = self.browser.find_element_by_class_name("blog_post")
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_title").text,
         "My first blog post"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_date").text,
         "10 October, 1962"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_body").text,
         "My first blog post!"
        )

        # The fan goes to the blog page
        self.browser.get(self.live_server_url + "/blog")

        # There is one blog post, and it's the same one
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 1)
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "My first blog post"
        )
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_date").text,
         "10 October, 1962"
        )
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_body").text,
         "My first blog post!"
        )

        # The fan goes away
        self.browser.quit()

        # Sam decides to write a new blog post
        self.browser = webdriver.Chrome()
        self.sam_writes_blog_post(
         "My second blog post",
         "11101962",
         "My second blog post!",
         True
        )
        self.browser.quit()

        # The fan comes back, and sees the new post on the home page
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        blog_post = self.browser.find_element_by_class_name("blog_post")
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_title").text,
         "My second blog post"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_date").text,
         "11 October, 1962"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_body").text,
         "My second blog post!"
        )

        # They go to the blog page, and there are two posts there
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 2)

        # They are in the correct order
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "My second blog post"
        )
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_title").text,
         "My first blog post"
        )

        # The fan goes away again
        self.browser.quit()

        # Sam writes a third post, but he isn't sure so doesn't make it visible
        self.browser = webdriver.Chrome()
        self.sam_writes_blog_post(
         "My third blog post",
         "12101962",
         "My third blog post!",
         False
        )
        self.browser.quit()

        # The fan comes back, but only the second post is visible
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        blog_post = self.browser.find_element_by_class_name("blog_post")
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_title").text,
         "My second blog post"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_date").text,
         "11 October, 1962"
        )
        self.assertEqual(
         blog_post.find_element_by_class_name("blog_post_body").text,
         "My second blog post!"
        )

        # On the blog page, there are still only two posts
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 2)


    def test_sam_can_edit_and_delete_blogs(self):
        # Sam writes three blog posts
        self.sam_writes_blog_post(
         "First post",
         "28071914",
         "Start",
         True
        )
        self.sam_writes_blog_post(
         "Second post",
         "01071916",
         "Middle",
         True
        )
        self.sam_writes_blog_post(
         "Third post",
         "11111918",
         "End",
         False
        )
        self.browser.quit()

        # A wild fan appears, and peruses the blog page
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 2)
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "Second post"
        )
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_title").text,
         "First post"
        )
        self.browser.quit()

        # Sam goes to the edit blog page
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog/edit")

        # There is a table there, with all the blog posts
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[0].text,
         "Third post"
        )
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[-1].text,
         "No"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[0].text,
         "Second post"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[-1].text,
         "Yes"
        )
        self.assertEqual(
         rows[2].find_elements_by_tag_name("td")[0].text,
         "First post"
        )
        self.assertEqual(
         rows[2].find_elements_by_tag_name("td")[-1].text,
         "Yes"
        )

        # Sam makes the third post visible
        rows[0].click()
        self.assertRegex(
         self.browser.current_url,
         self.live_server_url + r"/blog/edit/\d+/$"
        )
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        date_entry = form.find_elements_by_tag_name("input")[1]
        body_entry = form.find_element_by_tag_name("textarea")
        live_box = form.find_elements_by_tag_name("input")[2]
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.assertEqual(
         title_entry.get_attribute("value"),
         "Third post"
        )
        self.assertEqual(
         date_entry.get_attribute("value"),
         "1918-11-11"
        )
        self.assertEqual(
         body_entry.get_attribute("value"),
         "End"
        )
        self.assertFalse(live_box.is_selected())
        live_box.click()
        submit_button.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/blog/")
        self.browser.quit()

        # The third post is now visible
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 3)
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "Third post"
        )
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_title").text,
         "Second post"
        )
        self.assertEqual(
         blog_posts[2].find_element_by_class_name("blog_post_title").text,
         "First post"
        )
        self.browser.quit()

        # Sam wants to delete the second post - he goes to the edit page for it
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog/edit")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)
        rows[1].click()

        # There is a delete button after the form - he presses it
        delete_button = self.browser.find_element_by_tag_name("button")
        delete_button.click()

        # Now he is on a deletion page, and is asked if he is sure
        self.assertRegex(
         self.browser.current_url,
         self.live_server_url + r"/blog/edit/\d+/delete$"
        )
        form = self.browser.find_element_by_tag_name("form")
        warning = form.find_element_by_id("warning")
        self.assertIn(
         "are you sure?",
         warning.text.lower()
        )

        # There is a back to safety link, and a delete button
        back_to_safety = form.find_elements_by_tag_name("a")
        delete_button = form.find_element_by_tag_name("input")

        # He deletes, and is taken back to the edit page
        delete_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/edit"
        )

        # Now there are two rows
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_element_by_class_name("tr")
        self.assertEqual(len(rows), 2)
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "Third post"
        )
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_title").text,
         "First post"
        )
        self.browser.quit()

        # A user goes to the blog page and finds two posts there
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 2)
        self.assertEqual(
         blog_posts[0].find_element_by_class_name("blog_post_title").text,
         "Third post"
        )
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_title").text,
         "First post"
        )
        self.browser.quit()

        # Sam edits the first post to have a different body
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/edit")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_element_by_class_name("tr")
        self.assertEqual(len(rows), 2)
        rows[1].click()
        form = self.browser.find_element_by_tag_name("form")
        body_entry = form.find_element_by_tag_name("textarea")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        body_entry.clear()
        body_entry.send_keys("A modified body")
        submit_button.click()
        self.browser.quit()

        # The user sees the modified body
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        self.assertEqual(len(blog_posts), 2)
        self.assertEqual(
         blog_posts[1].find_element_by_class_name("blog_post_body").text,
         "A modified body"
        )
        self.browser.quit()
