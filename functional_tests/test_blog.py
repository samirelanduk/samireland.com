import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class BlogTest(FunctionalTest):

    def sam_writes_blog_post(self, title, date, body, visible, check_redirect=True):
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
        if check_redirect:
            self.assertEqual(
             self.browser.current_url,
             self.live_server_url + "/"
            )


    def get_home_blog_post_content(self):
        self.browser.get(self.live_server_url)
        blog_post = self.browser.find_element_by_class_name("blog_post")
        return [
         blog_post.find_element_by_class_name("blog_post_title").text,
         blog_post.find_element_by_class_name("blog_post_date").text,
         blog_post.find_element_by_class_name("blog_post_body").text
        ]


    def get_blog_page_posts_content(self):
        self.browser.get(self.live_server_url + "/blog/")
        blog_posts = self.browser.find_elements_by_class_name("blog_post")
        return [[
         blog_post.find_element_by_class_name("blog_post_title").text,
         blog_post.find_element_by_class_name("blog_post_date").text,
         blog_post.find_element_by_class_name("blog_post_body").text
        ] for blog_post in blog_posts]



class BlogContentTest(BlogTest):

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
         "http://github.com/samirelanduk/",
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



class NewBlogTest(BlogTest):

    def test_sam_can_write_blog_post(self):
        # Sam posts a first blog post
        self.sam_writes_blog_post(
         "My first blog post",
         "10101962",
         "My first blog post!",
         True
        )

        # Sam goes away, another mighty victory achieved
        self.browser.quit()

        # One of Sam's many fans comes to the site, and checks the home page
        self.browser = webdriver.Chrome()

        # There is the blog post
        self.assertEqual(
         self.get_home_blog_post_content(),
         ["My first blog post", "10 October, 1962", "My first blog post!"]
        )

        # The fan goes to the blog page, and sees the same post there
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [["My first blog post", "10 October, 1962", "My first blog post!"]]
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
        self.assertEqual(
         self.get_home_blog_post_content(),
         ["My second blog post", "11 October, 1962", "My second blog post!"]
        )

        # They go to the blog page, and there are two posts there
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["My second blog post", "11 October, 1962", "My second blog post!"],
          ["My first blog post", "10 October, 1962", "My first blog post!"]
         ]
        )

        # The fan goes away again
        self.browser.quit()


    def test_sam_can_post_hidden_blog_posts(self):
        # Sam makes three blog posts, one hidden
        self.sam_writes_blog_post(
         "My first blog post",
         "10101962",
         "My first blog post!",
         True
        )
        self.sam_writes_blog_post(
         "My second blog post",
         "11101962",
         "My second blog post!",
         True
        )
        self.sam_writes_blog_post(
         "My third blog post",
         "12101962",
         "My third blog post!",
         False
        )
        self.browser.quit()

        # The fan comes back, but only the second post is visible
        self.browser = webdriver.Chrome()
        self.assertEqual(
         self.get_home_blog_post_content(),
         ["My second blog post", "11 October, 1962", "My second blog post!"]
        )

        # On the blog page, there is only two posts
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["My second blog post", "11 October, 1962", "My second blog post!"],
          ["My first blog post", "10 October, 1962", "My first blog post!"]
         ]
        )



class EditBlogTest(BlogTest):

    def test_sam_can_edit_blog_posts(self):
        # Sam writes three blog posts
        self.sam_writes_blog_post("First post", "28071914", "Start", True)
        self.sam_writes_blog_post("Second post", "01071916", "Middle", True)
        self.sam_writes_blog_post("Third post", "11111918", "End", True)
        self.browser.quit()

        # A wild fan appears, and peruses the blog page
        self.browser = webdriver.Chrome()
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["Third post", "11 November, 1918", "End"],
          ["Second post", "1 July, 1916", "Middle"],
          ["First post", "28 July, 1914", "Start"]
         ]
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
         "Yes"
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

        # Sam makes the third post invisible
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
        self.assertTrue(live_box.is_selected())
        live_box.click()
        submit_button.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + "/blog/")
        self.browser.quit()

        # The third post is now invisible
        self.browser = webdriver.Chrome()
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["Second post", "1 July, 1916", "Middle"],
          ["First post", "28 July, 1914", "Start"]
         ]
        )
        self.browser.quit()

        # Sam edits the first post to have a different body
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog/edit/")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        rows[-1].click()
        form = self.browser.find_element_by_tag_name("form")
        body_entry = form.find_element_by_tag_name("textarea")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        body_entry.clear()
        body_entry.send_keys("A modified body")
        submit_button.click()
        self.browser.quit()

        # The user sees the modified body
        self.browser = webdriver.Chrome()
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["Second post", "1 July, 1916", "Middle"],
          ["First post", "28 July, 1914", "A modified body"]
         ]
        )


    def test_sam_can_delete_blog_posts(self):
        # Sam writes three blog posts
        self.sam_writes_blog_post("First post", "28071914", "Start", True)
        self.sam_writes_blog_post("Second post", "01071916", "Middle", True)
        self.sam_writes_blog_post("Third post", "11111918", "End", True)
        self.browser.quit()

        # Sam wants to delete the second post - he goes to the edit page for it
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url + "/blog/edit")
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 3)
        rows[1].click()

        # There is a delete button after the form - he presses it
        delete_button = self.browser.find_element_by_id("delete")
        delete_button.click()

        # Now he is on a deletion page, and is asked if he is sure
        self.assertRegex(
         self.browser.current_url,
         self.live_server_url + r"/blog/delete/\d+/$"
        )
        form = self.browser.find_element_by_tag_name("form")
        warning = form.find_element_by_id("warning")
        self.assertIn(
         "are you sure?",
         warning.text.lower()
        )

        # There is a back to safety link, and a delete button
        back_to_safety = form.find_element_by_tag_name("a")
        delete_button = form.find_elements_by_tag_name("input")[-1]

        # He deletes, and is taken back to the edit page
        delete_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/edit/"
        )

        # Now there are two rows
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[1:]
        self.assertEqual(len(rows), 2)
        self.assertEqual(
         rows[0].find_elements_by_tag_name("td")[0].text,
         "Third post"
        )
        self.assertEqual(
         rows[1].find_elements_by_tag_name("td")[0].text,
         "First post"
        )
        self.browser.quit()

        # A user goes to the blog page and finds two posts there
        self.browser = webdriver.Chrome()
        self.assertEqual(
         self.get_blog_page_posts_content(),
         [
          ["Third post", "11 November, 1918", "End"],
          ["First post", "28 July, 1914", "Start"]
         ]
        )



class BlogValidationTests(BlogTest):

    def test_sam_cannot_post_blank_blog_post(self):
        # Sam makes a post with no title
        self.sam_writes_blog_post("", "10101962", "TEST", True,
         check_redirect=False)

        # He is still on the new page!
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/new/"
        )

        # There is an error message saying there needs to be a title
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no title"
        )

        # Sam makes a post with no date
        self.sam_writes_blog_post("Title", "", "TEST", True,
         check_redirect=False)

        # He is still on the new page!
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/new/"
        )

        # There is an error message saying there needs to be a date
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no date"
        )

        # Sam makes a post with no body
        self.sam_writes_blog_post("Title", "10101962", "", True, check_redirect=False)

        # He is still on the new page!
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/new/"
        )

        # There is an error message saying there needs to be a body
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no body"
        )


    def test_sam_cannot_edit_a_post_to_have_blank_fields(self):
        # Sam writes a blog post
        self.sam_writes_blog_post("Title", "10101962", "TEST", True)

        # He decides to edit it
        self.browser.get(self.live_server_url + "/blog/edit/")
        row = self.browser.find_elements_by_tag_name("tr")[-1]
        row.click()
        edit_url = self.browser.current_url
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        title_entry.clear()

        # He tries to save it, but can't
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()
        self.assertEqual(
         self.browser.current_url,
         edit_url
        )

        # There is an error message saying there needs to be a title
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no title"
        )

        # He tries to do the same with the body, which also fails
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        title_entry.send_keys("...")
        body_entry = form.find_element_by_tag_name("textarea")
        body_entry.clear()
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()
        self.assertEqual(
         self.browser.current_url,
         edit_url
        )
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no body"
        )


    def test_sam_cannot_have_two_posts_with_same_date(self):
        # Sam makes two blog posts
        self.sam_writes_blog_post("Post 1", "10102012", "TEST", True)
        self.sam_writes_blog_post("Post 2", "11102012", "TEST", True)

        # He tries to write a third blog post with the same data as the second
        self.sam_writes_blog_post("Post 3", "11102012", "TEST", True, check_redirect=False)

        # But he can't
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/blog/new/"
        )
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "There is already a blog post for this date"
        )


    def test_sam_cannot_edit_a_post_to_have_existing_date(self):
        # Sam makes two blog posts
        self.sam_writes_blog_post("Post 1", "10102012", "TEST", True)
        self.sam_writes_blog_post("Post 2", "11102012", "TEST", True)

        # He decides to edit an existing post
        self.browser.get(self.live_server_url + "/blog/edit/")
        row = self.browser.find_elements_by_tag_name("tr")[1]
        row.click()
        edit_url = self.browser.current_url
        form = self.browser.find_element_by_tag_name("form")
        date_entry = form.find_elements_by_tag_name("input")[1]
        date_entry.send_keys("10102012")
        submit_button = form.find_elements_by_tag_name("input")[-1]
        submit_button.click()
        self.assertEqual(
         self.browser.current_url,
         edit_url
        )

        # And this fails to work
        self.assertEqual(
         self.browser.current_url,
         edit_url
        )
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "There is already a blog post for this date"
        )


    def test_error_messages_disappear_after_typing(self):
        # Sam makes a post with no title
        self.sam_writes_blog_post("", "10101962", "TEST", True,
         check_redirect=False)

        # There is an error message saying there needs to be a title
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no title"
        )

        # Sam begins to type in the title box
        form = self.browser.find_element_by_tag_name("form")
        title_entry = form.find_elements_by_tag_name("input")[0]
        title_entry.send_keys("T")

        # The error message vanishes
        error = self.browser.find_element_by_class_name("error")
        self.assertFalse(error.is_displayed())

        # Sam makes a post with no body
        self.sam_writes_blog_post("Title", "10101962", "", True,
         check_redirect=False)

        # There is an error message saying there needs to be a title
        error = self.browser.find_element_by_class_name("error")
        self.assertEqual(
         error.text,
         "You cannot submit a blog post with no body"
        )

        # Sam begins to type in the title box
        form = self.browser.find_element_by_tag_name("form")
        body_entry = form.find_elements_by_tag_name("input")[2]
        body_entry.send_keys("B")

        # The error message vanishes
        error = self.browser.find_element_by_class_name("error")
        self.assertFalse(error.is_displayed())



class BlogFormattingTests(BlogTest):

    def test_blog_post_has_paragraphs(self):
        # Sam writes a post with three paragraphs
        self.sam_writes_blog_post(
         "Three Paragraph Post",
         "01012016",
         "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3.",
         True
        )

        # He goes to the home page and sees a post, with three paragraphs
        self.browser.get(self.live_server_url + "/")
        blog_post_body = self.browser.find_element_by_class_name("blog_post_body")
        paragraphs = blog_post_body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0].text, "Paragraph 1.")
        self.assertEqual(paragraphs[1].text, "Paragraph 2.")
        self.assertEqual(paragraphs[2].text, "Paragraph 3.")


    def test_blog_post_italics_bold_underline(self):
        # Sam writes three blog posts with formatting
        self.sam_writes_blog_post(
         "Three Paragraph Post",
         "01012016",
         "Para*graph* 1.\n\n\nPara_graph_ 2.\n\n\n\nPara**graph** 3",
         True
        )

        # He goes to the home page and sees a post, with three paragraphs
        self.browser.get(self.live_server_url + "/")
        blog_post_body = self.browser.find_element_by_class_name("blog_post_body")
        paragraphs = blog_post_body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0].find_element_by_tag_name("em").text, "graph")
        self.assertEqual(paragraphs[1].find_element_by_tag_name("u").text, "graph")
        self.assertEqual(paragraphs[2].find_element_by_tag_name("b").text, "graph")


    def test_blog_post_hyperlinks(self):
        # Sam writes a blog post with two links, one to open in a new page
        self.sam_writes_blog_post(
         "Three Paragraph Post",
         "01012016",
         "Here is a [link](http://hogwarts.ac.uk/the_sorting_hat/).\n\n[link2](http://test.com/ newpage])",
         True
        )

        # He goes to the home page and sees a post, with three paragraphs
        self.browser.get(self.live_server_url + "/")
        blog_post_body = self.browser.find_element_by_class_name("blog_post_body")
        paragraphs = blog_post_body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Here is a link.")
        self.assertEqual(paragraphs[0].find_element_by_tag_name("a").text, "link")
        self.assertEqual(
         paragraphs[0].find_element_by_tag_name("a").get_attribute("href"),
         "http://hogwarts.ac.uk/the_sorting_hat/"
        )
        self.assertEqual(paragraphs[1].find_element_by_tag_name("a").text, "link2")
        self.assertEqual(
         paragraphs[0].find_element_by_tag_name("a").get_attribute("href"),
         "http://test.com/"
        )
        self.assertEqual(
         paragraphs[0].find_element_by_tag_name("a").get_attribute("target"),
         "_blank"
        )
