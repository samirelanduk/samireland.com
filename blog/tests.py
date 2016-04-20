from django.test import TestCase
from blog import views
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.models import BlogPost
import datetime

# Create your tests here.
class UrlTests(TestCase):

    def check_url_returns_view(self, url, view):
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, view)


    def test_root_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/", views.home_page)


    def test_about_url_resolves_to_about_view(self):
        self.check_url_returns_view("/about/", views.about_page)


    def test_blog_url_resolves_to_blog_view(self):
        self.check_url_returns_view("/blog/", views.blog_page)


    def test_new_url_resolves_to_new_view(self):
        self.check_url_returns_view("/blog/new/", views.new_post_page)


    def test_edit_url_resolves_to_edit_post(self):
        self.check_url_returns_view("/blog/edit/", views.edit_posts_page)



class ViewTests(TestCase):

    def check_view_uses_template(self, view, template):
        request = HttpRequest()
        response = view(request)
        expected_html = render_to_string(template)
        self.assertEqual(response.content.decode(), expected_html)


    def make_post_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["title"] = "."
        request.POST["date"] = "1939-09-01"
        request.POST["body"] = "."
        request.POST["visible"] = True
        return request


    def get_html_after_three_blog_posts(self, view, last_invisible=False):
        for date in (
         datetime.datetime(1950,1,1),
         datetime.datetime(1960,1,1),
         datetime.datetime(1955,1,1)
        ):
            post = BlogPost(
             date=date, title=".", body=".",
             visible=not(last_invisible and date == datetime.datetime(1960,1,1))
            )
            post.save()
        if last_invisible:
            BlogPost.objects
        request = HttpRequest()
        return view(request).content.decode()


    def test_home_page_view_uses_home_page_template(self):
        self.check_view_uses_template(views.home_page, "home.html")


    def test_home_view_uses_most_recent_blog_post(self):
        home_html = self.get_html_after_three_blog_posts(views.home_page)
        self.assertIn("1960", home_html)
        self.assertNotIn("1950", home_html)
        self.assertNotIn("1955", home_html)


    def test_home_view_ignores_invisible_posts(self):
        home_html = self.get_html_after_three_blog_posts(views.home_page, last_invisible=True)
        self.assertIn("1955", home_html)
        self.assertNotIn("1950", home_html)
        self.assertNotIn("1960", home_html)


    def test_about_page_view_uses_about_page_template(self):
        self.check_view_uses_template(views.about_page, "about.html")


    def test_blog_page_view_uses_blog_page_template(self):
        self.check_view_uses_template(views.blog_page, "blog.html")


    def test_blog_page_shows_posts_in_correct_order(self):
        blog_html = self.get_html_after_three_blog_posts(views.blog_page)
        pos_1950 = blog_html.find("January, 1950")
        pos_1955 = blog_html.find("January, 1955")
        pos_1960 = blog_html.find("January, 1960")
        self.assertTrue(pos_1960 < pos_1955 < pos_1950)


    def test_blog_page_ignores_invisible_posts(self):
        blog_html = self.get_html_after_three_blog_posts(views.blog_page, last_invisible=True)
        pos_1950 = blog_html.find("January, 1950")
        pos_1955 = blog_html.find("January, 1955")
        pos_1960 = blog_html.find("January, 1960")
        self.assertTrue(pos_1955 < pos_1950)
        self.assertEqual(pos_1960, -1)


    def test_new_post_view_uses_new_post_template(self):
        self.check_view_uses_template(views.new_post_page, "new_post.html")


    def test_new_post_view_can_save_blog_post(self):
        self.assertEqual(BlogPost.objects.count(), 0)
        request = self.make_post_request()
        views.new_post_page(request)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, ".")


    def test_new_post_view_redirects_after_POST(self):
        request = self.make_post_request()
        response = views.new_post_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")


    def test_edit_post_view_uses_edit_post_template(self):
        self.check_view_uses_template(views.edit_posts_page, "edit_posts.html")


    def test_edit_post_view_shows_all_posts_in_correct_order(self):
        html = self.get_html_after_three_blog_posts(views.edit_posts_page, last_invisible=True)
        pos_1950 = html.find("January, 1950")
        pos_1955 = html.find("January, 1955")
        pos_1960 = html.find("January, 1960")
        self.assertTrue(pos_1960 < pos_1955 < pos_1950)


class ModelTests(TestCase):

    def test_save_and_retrieve_BlogPost(self):
        self.assertEqual(BlogPost.objects.all().count(), 0)
        blog_post = BlogPost()
        blog_post.title = "A post"
        blog_post.date = datetime.datetime(1939, 9, 1, 5, 0, 0)
        blog_post.body = "Blah blah blah"
        blog_post.visible = False
        blog_post.save()
        self.assertEqual(BlogPost.objects.all().count(), 1)

        retrieved_post = BlogPost.objects.first()
        self.assertEqual(retrieved_post, blog_post)


    def test_cannot_create_post_without_parameters(self):
        params = {
         "title":".",
         "date":datetime.datetime.now(),
         "body":".",
         "visible":True
        }
        param_names = list(params.keys())
        param_names.remove("visible")
        for i in range(len(param_names)):
            incomplete_params = params.copy()
            del incomplete_params[param_names[i]]
            blog_post = BlogPost(**incomplete_params)
            self.assertRaises(ValidationError, blog_post.full_clean)
