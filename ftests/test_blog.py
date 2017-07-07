"""Contains tests for the blog section."""

from time import sleep
from datetime import datetime
from blog.models import BlogPost
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
        BlogPost.objects.create(
         date=datetime(2009, 5, 22).date(), title="Vanq", body="B\n\nB", visible=False
        )
        BlogPost.objects.create(
         date=datetime(2009, 4, 4).date(), title="Com", body="C\n\nC", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2009, 4, 28).date(), title="Fin", body="F\n\nF", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2010, 1, 9).date(), title="Siq", body="B\n\nB", visible=False
        )
        BlogPost.objects.create(
         date=datetime(2010, 1, 11).date(), title="Zed", body="Z\n\nZ", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2010, 2, 10).date(), title="DD", body="D\n\nD", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2010, 5, 23).date(), title="Uty", body="U\n\nU", visible=True
        )


    def test_can_cycle_between_blog_posts(self):
        self.browser.set_window_size(800, 600)
        self.get("/")

        # The user clicks the blog link in the header
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[4].click()
        self.check_page("/blog/")

        # There are five blog posts there (visible only)
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 5)

        # Details are correct and in order
        self.check_blog_post(
         posts[0], "23 May, 2010", "Uty", ["U", "U"], True
        )
        self.check_blog_post(
         posts[1], "10 February, 2010", "DD", ["D", "D"], True
        )
        self.check_blog_post(
         posts[2], "11 January, 2010", "Zed", ["Z", "Z"], True
        )
        self.check_blog_post(
         posts[3], "28 April, 2009", "Fin", ["F", "F"], True
        )
        self.check_blog_post(
         posts[4], "4 April, 2009", "Com", ["C", "C"], True
        )

        # The user clicks the title of the first post
        title = posts[0].find_element_by_class_name("post-title")
        title.find_element_by_tag_name("a").click()
        self.check_page("/blog/2010/5/23/")

        # There is a single blog post on the page
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "23 May, 2010", "Uty", ["U", "U"], True
        )

        # There is a link to the previous post but not one to the next
        previous_link = posts_section.find_element_by_id("previous-page")
        self.assertEqual(len(posts_section.find_elements_by_id("next-page")), 0)

        # They click through to the end
        previous_link.click()
        self.check_page("/blog/2010/2/10/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "10 February, 2010", "DD", ["D", "D"], True
        )
        previous_link = posts_section.find_element_by_id("previous-page")
        next_link = posts_section.find_element_by_id("next-page")

        previous_link.click()
        self.check_page("/blog/2010/1/11/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "11 January, 2010", "Zed", ["Z", "Z"], True
        )
        previous_link = posts_section.find_element_by_id("previous-page")
        next_link = posts_section.find_element_by_id("next-page")

        previous_link.click()
        self.check_page("/blog/2009/4/28/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "28 April, 2009", "Fin", ["F", "F"], True
        )
        previous_link = posts_section.find_element_by_id("previous-page")
        next_link = posts_section.find_element_by_id("next-page")

        previous_link.click()
        self.check_page("/blog/2009/4/4/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "4 April, 2009", "Com", ["C", "C"], True
        )
        self.assertEqual(len(posts_section.find_elements_by_id("previous-post")), 0)
        next_link = posts_section.find_element_by_id("next-page")

        # They can also go back
        next_link.click()
        self.check_page("/blog/2009/4/28/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "28 April, 2009", "Fin", ["F", "F"], True
        )

        # They login and go back to the blog page
        self.login()
        self.get("/blog/")

        # There are seven blog posts there (all now)
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 7)

        # The posts are all correct
        self.check_blog_post(
         posts[0], "23 May, 2010", "Uty", ["U", "U"], True
        )
        self.check_blog_post(
         posts[1], "10 February, 2010", "DD", ["D", "D"], True
        )
        self.check_blog_post(
         posts[2], "11 January, 2010", "Zed", ["Z", "Z"], True
        )
        self.check_blog_post(
         posts[3], "9 January, 2010", "Siq", ["B", "B"], False
        )
        self.check_blog_post(
         posts[4], "22 May, 2009", "Vanq", ["B", "B"], False
        )
        self.check_blog_post(
         posts[5], "28 April, 2009", "Fin", ["F", "F"], True
        )
        self.check_blog_post(
         posts[6], "4 April, 2009", "Com", ["C", "C"], True
        )

        # The invisible titles are not links
        title = posts[3].find_element_by_class_name("post-title")
        self.assertEqual(len(title.find_elements_by_tag_name("a")), 0)
        title = posts[4].find_element_by_class_name("post-title")
        self.assertEqual(len(title.find_elements_by_tag_name("a")), 0)

        # The invisible posts are not navigable to
        title = posts[2].find_element_by_class_name("post-title")
        title.find_element_by_tag_name("a").click()
        self.check_page("/blog/2010/1/11/")
        previous = self.browser.find_element_by_id("previous-page")
        previous.click()
        self.check_page("/blog/2009/4/28/")
        next_ = self.browser.find_element_by_id("next-page")
        next_.click()
        self.check_page("/blog/2010/1/11/")


    def test_can_get_blog_posts_by_period(self):
        BlogPost.objects.create(
         date=datetime(2011, 5, 23).date(), title="Uty", body="U\n\nU", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2012, 5, 23).date(), title="Uty", body="U\n\nU", visible=False
        )

        # The user goes to the home page and hovers over the blog link
        self.browser.set_window_size(800, 600)
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.hover(nav_links[4])

        # There are now links to individual years
        year_links = nav.find_element_by_id("year-links")
        years = year_links.find_elements_by_class_name("blog-year")
        self.assertEqual(years[0].text, "2011")
        self.assertEqual(years[1].text, "2010")
        self.assertEqual(years[2].text, "2009")
        self.assertAlmostEqual(
         years[0].location["x"], nav_links[4].location["x"], delta=15
        )

        # The user moves away and they vanish
        self.hover(nav_links[0])

        # They bring them back
        self.hover(nav_links[4])
        year_links = nav.find_element_by_id("year-links")
        years = year_links.find_elements_by_class_name("blog-year")

        # They click on the top link and go to the page for that year
        years[0].click()
        self.check_page("/blog/2011/")
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "2011")

        # There is one post here
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.check_blog_post(
         posts[0], "23 May, 2011", "Uty", ["U", "U"], True
        )

        # There is a link to the previous year but not one to the next
        previous_link = posts_section.find_element_by_id("previous-page")
        self.assertEqual(len(posts_section.find_elements_by_id("next-page")), 0)
        self.assertEqual(previous_link.text[-4:], "2010")

        # They click through to the end
        previous_link.click()
        self.check_page("/blog/2010/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 3)
        self.check_blog_post(
         posts[0], "23 May, 2010", "Uty", ["U", "U"], True
        )
        self.check_blog_post(
         posts[1], "10 February, 2010", "DD", ["D", "D"], True
        )
        self.check_blog_post(
         posts[2], "11 January, 2010", "Zed", ["Z", "Z"], True
        )
        previous_link = posts_section.find_element_by_id("previous-page")
        next_link = posts_section.find_element_by_id("next-page")
        self.assertEqual(previous_link.text[-4:], "2009")
        self.assertEqual(next_link.text[:4], "2011")

        previous_link.click()
        self.check_page("/blog/2009/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 2)
        self.check_blog_post(
         posts[0], "28 April, 2009", "Fin", ["F", "F"], True
        )
        self.check_blog_post(
         posts[1], "4 April, 2009", "Com", ["C", "C"], True
        )
        self.assertEqual(len(posts_section.find_elements_by_id("previous-post")), 0)
        next_link = posts_section.find_element_by_id("next-page")
        self.assertEqual(next_link.text[:4], "2010")

        # They can also go back
        next_link.click()
        self.check_page("/blog/2010/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 3)
        self.check_blog_post(
         posts[0], "23 May, 2010", "Uty", ["U", "U"], True
        )
        self.check_blog_post(
         posts[1], "10 February, 2010", "DD", ["D", "D"], True
        )
        self.check_blog_post(
         posts[2], "11 January, 2010", "Zed", ["Z", "Z"], True
        )



class BlogModificationTests(BlogTest):

    def setUp(self):
        BlogTest.setUp(self)
        BlogPost.objects.create(
         date=datetime(2009, 5, 22).date(), title="Vanq", body="B\n\nB", visible=True
        )
        BlogPost.objects.create(
         date=datetime(2009, 4, 30).date(), title="Com", body="C\n\nC", visible=False
        )
        BlogPost.objects.create(
         date=datetime(2009, 4, 28).date(), title="Fin", body="F\n\nF", visible=True
        )


    def test_can_modify_blog_post(self):
        # The user goes to the blog page
        self.get("/blog/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 2)

        # The posts don't have edit links
        for post in posts:
            self.assertFalse(post.find_elements_by_class_name("edit-post-link"))

        # The user logs in and now they do
        self.login()
        self.get("/blog/")
        posts_section = self.browser.find_element_by_id("posts")
        posts = posts_section.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 3)
        for post in posts[::-1]:
            edit_link = post.find_element_by_class_name("edit-post-link")

        # The user clicks the edit link for the first post
        edit_link.click()
        self.check_page("/blog/2009/5/22/edit/")
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, "Edit Blog Post")
        form = self.browser.find_element_by_tag_name("form")
        date_input, title_input = form.find_elements_by_tag_name("input")[:2]
        body_input = form.find_element_by_tag_name("textarea")
        visible_input = form.find_elements_by_tag_name("input")[2]
        visible_label = form.find_element_by_tag_name("label")
        self.assertEqual(date_input.get_attribute("type"), "date")
        self.assertEqual(date_input.get_attribute("value"), "2009-05-22")
        self.assertEqual(title_input.get_attribute("type"), "text")
        self.assertEqual(title_input.get_attribute("value"), "Vanq")
        self.assertEqual(body_input.get_attribute("value"), "B\n\nB")
        self.assertEqual(visible_input.get_attribute("type"), "checkbox")
        self.assertTrue(visible_input.is_selected())

        # The user edits the title, date and body of the post

        # The user is now on the post's page, and it looks great

        # The user goes back to the blog page

        # The user makes the invisible post visible


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
