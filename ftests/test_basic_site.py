import os
from django.core.files.uploadedfile import SimpleUploadedFile
from .base import FunctionalTest
from samireland.settings import MEDIA_ROOT
from samireland.models import *

class SiteLayoutTests(FunctionalTest):

    def test_page_layout(self):
        # All the right elements are there
        self.get("/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )

        # The header has the name in it
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(header.text, "Sam Ireland")

        # The nav has a list of links
        nav = self.browser.find_element_by_tag_name("nav")
        ul = nav.find_element_by_tag_name("ul")
        links = ul.find_elements_by_tag_name("li")
        self.assertEqual(links[0].text, "Home")
        self.assertEqual(links[1].text, "Research")
        self.assertEqual(links[2].text, "Projects")
        self.assertEqual(links[3].text, "Writing")
        self.assertEqual(links[4].text, "Blog")
        self.assertEqual(links[5].text, "About")

        # The footer has a bunch of icons
        footer = self.browser.find_element_by_tag_name("footer")
        icons = footer.find_elements_by_class_name("social-icon")
        self.assertGreaterEqual(len(icons), 4)



class HomePageTests(FunctionalTest):

    def test_home_page_structure(self):
        # The user goes to the home page
        self.get("/")
        self.check_title("Home")


        # There is an introductory section
        intro = self.browser.find_element_by_class_name("intro")
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("form")

        # There are latest sections
        blog = self.browser.find_element_by_id("latest-blog")
        article = self.browser.find_element_by_id("latest-article")
        pub = self.browser.find_element_by_id("latest-pub")
        self.assertIn("no blog posts", blog.text)
        self.assertIn("no articles", article.text)
        self.assertIn("no publications", pub.text)


    def test_latest_entries(self):
        BlogPost.objects.create(date="2017-01-01", title="T1", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-03", title="T2", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-02", title="T3", body="1\n\n2")
        Article.objects.create(
         id="article-1", title="The First Article", date="2016-01-01",
         summary="summary1", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-2", title="The Recent Article", date="2016-08-09",
         summary="summary2", body="Line 1\n\nLine 2"
        )
        Article.objects.create(
         id="article-3", title="The Middle Article", date="2016-04-12",
         summary="summary3", body="Line 1\n\nLine 2"
        )
        Publication.objects.create(
         id="paper-1", title="The First Paper", date="2016-01-01",
         url="www.com", doi="DDD", authors="Jack, Jill",
         body="Line 1\n\nLine 2"
        )
        Publication.objects.create(
         id="paper-2", title="The Recent Paper", date="2016-08-09",
         url="www.com", doi="DDD2", authors="Jack, Jill, Bob",
         body="Line 1\n\nLine 2"
        )
        Publication.objects.create(
         id="paper-3", title="The Middle Paper", date="2016-04-12",
         url="www.com", doi="DDD3", authors="Jack, Sally",
         body="Line 1\n\nLine 2"
        )

        # There are latest sections on the home page
        self.get("/")
        blog = self.browser.find_element_by_id("latest-blog")
        article = self.browser.find_element_by_id("latest-article")
        pub = self.browser.find_element_by_id("latest-pub")

        # The latest blog post is there
        post = blog.find_element_by_class_name("blog-post")
        self.assertNotIn("no blog posts", blog.text)
        date = post.find_element_by_class_name("date")
        title = post.find_element_by_tag_name("h3")
        self.assertEqual(date.text, "3 January, 2017")
        self.assertEqual(title.text, "T2")
        body = post.find_element_by_class_name("post-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "1")
        self.assertEqual(paragraphs[1].text, "2")
        with self.assertRaises(self.NoElement):
            post.find_element_by_id("posts-nav")

        # The latest article is there
        article = article.find_element_by_class_name("blog-post")
        self.assertNotIn("no articles", article.text)
        self.assertEqual(
         article.find_element_by_class_name("article-title").text,
         "The Recent Article"
        )
        self.assertEqual(
         article.find_element_by_class_name("date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         article.find_element_by_class_name("article-summary").text,
         "summary2"
        )
        self.assertEqual(
         article.find_element_by_class_name("article-link").text,
         "Read More"
        )

        # The latest publication is there
        pub = pub.find_element_by_class_name("blog-post")
        self.assertNotIn("no publications", pub.text)
        self.assertEqual(
         pub.find_element_by_tag_name("h3").text,
         "The Recent Paper"
        )
        self.assertEqual(
         pub.find_element_by_class_name("date").text,
         "9 August, 2016"
        )
        self.assertEqual(
         pub.find_element_by_class_name("pub-authors").text,
         "Jack, Jill, Bob"
        )
        self.assertEqual(
         pub.find_element_by_class_name("pub-summary").text,
         "Read Summary"
        )



class AboutPageTests(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass
        FunctionalTest.tearDown(self)


    def test_about_page_structure(self):
        # The user goes to the home page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[-1])
        self.check_title("About")

        # There's a heading and some about text
        self.check_h1("About Me")
        about = self.browser.find_element_by_class_name("about")
        with self.assertRaises(self.NoElement):
            about.find_element_by_tag_name("button")
        with self.assertRaises(self.NoElement):
            about.find_element_by_tag_name("form")


    def test_image_in_editable_text(self):
        mediafile = MediaFile.objects.create(
         name="test-image", mediafile=SimpleUploadedFile("test.png", b"\x00\x01")
        )
        EditableText.objects.create(name="about", body="![abc](test-image)")
        self.get("/about/")
        about = self.browser.find_element_by_class_name("about")
        image = about.find_element_by_tag_name("img")
        self.assertEqual(
         image.get_attribute("src"),
         self.live_server_url + "/" + mediafile.mediafile.url
        )
