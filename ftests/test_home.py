from time import sleep
import datetime
from random import randint
from .base import FunctionalTest
from blog.models import BlogPost

class BasePageLayoutTests(FunctionalTest):

    def test_base_layout_order(self):
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )


    def test_name_in_header(self):
        self.browser.get(self.live_server_url + "/")
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Sam Ireland", header.text)


    def test_nav_is_unordered_list_of_links(self):
        self.browser.get(self.live_server_url + "/")
        nav = self.browser.find_element_by_tag_name("nav")

        # The only child of the nav is a <ul>
        children = nav.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(3 <= len(children) <= 8)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            self.assertEqual(len(child.find_elements_by_tag_name("a")), 1)


    def test_footer_is_unordered_list_of_img_links(self):
        self.browser.get(self.live_server_url + "/")
        footer = self.browser.find_element_by_tag_name("footer")

        # The only child of the footer is a <ul>
        children = footer.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(2 <= len(children) <= 15)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            links = child.find_elements_by_tag_name("a")
            self.assertEqual(len(links), 1)
            self.assertIsNot(links[0].find_element_by_tag_name("img"), None)



class BasePageStyleTests(FunctionalTest):

    def test_header_and_nav_work_on_mobile(self):
        self.browser.get(self.live_server_url + "/")

        # The header is left aligned
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "start"
        )

        # There is a navicon to the right
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(header.location["y"], navicon.location["y"])
        self.assertLess(header.location["x"], navicon.location["x"])

        # The navbar itself isn't displayed
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # Clicking the navicon makes the nav appear
        navicon.click()
        self.assertNotEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # The links are in two columns
        links = navbar.find_elements_by_tag_name("li")
        self.assertEqual(len(set([link.location["x"] for link in links])), 2)

        # Clicking the navicon again makes the nav disappear
        navicon.click()
        sleep(1.5)
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # The user opens the page on an iPad
        self.browser.set_window_size(700, 900)
        self.browser.get(self.live_server_url + "/")

        # The basic layout is still the same
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "start"
        )
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(header.location["y"], navicon.location["y"])
        self.assertLess(header.location["x"], navicon.location["x"])
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertEqual(
         navbar.value_of_css_property("display"),
         "none"
        )

        # But the links are in three columns now
        navicon.click()
        self.assertNotEqual(
         navbar.value_of_css_property("display"),
         "none"
        )
        links = navbar.find_elements_by_tag_name("li")
        self.assertEqual(len(set([link.location["x"] for link in links])), 3)


    def test_header_and_nav_work_on_desktop(self):
        self.browser.set_window_size(800, 900)
        self.browser.get(self.live_server_url + "/")

        # The header is centred and there is no nav icon
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(
         header.value_of_css_property("text-align"),
         "center"
        )
        navicon = self.browser.find_element_by_id("navicon")
        self.assertEqual(
         navicon.value_of_css_property("display"),
         "none"
        )

        # The navbar is below it
        navbar = self.browser.find_element_by_tag_name("nav")
        self.assertGreater(navbar.location["y"], header.location["y"])

        # The links are all on one row
        links = navbar.find_elements_by_tag_name("li")
        first_link_y = links[0].location["y"]
        for link in links[1:]:
            self.assertAlmostEqual(link.location["y"], first_link_y, delta=4)



class HomePageTests(FunctionalTest):

    def test_can_change_home_page_text(self):
        self.check_can_edit_text("/", "brief-summary", "home")


    def test_cannot_access_home_edit_page_when_not_logged_in(self):
        self.get("/edit/home/")
        self.check_page("/")


    def test_blog_post_on_main_page(self):
        BlogPost.objects.create(
         date=datetime.datetime(2010, 1, 9).date(), title="Siq", body="B\n\nB", visible=True
        )
        BlogPost.objects.create(
         date=datetime.datetime(2010, 1, 11).date(), title="Zed", body="Z\n\nZ", visible=True
        )
        BlogPost.objects.create(
         date=datetime.datetime(2010, 2, 10).date(), title="DD", body="D\n\nD", visible=False
        )

        # They go to the main page
        self.get("/")

        # The most recent blog post is there
        latest_news = self.browser.find_element_by_id("latest-news")
        h2 = latest_news.find_element_by_tag_name("h2")
        self.assertEqual(h2.text, "Latest News")
        post = latest_news.find_element_by_class_name("blog-post")
        self.assertEqual(post.find_element_by_class_name("post-date").text, "11 January, 2010")
        self.assertEqual(post.find_element_by_class_name("post-title").text, "Zed")
