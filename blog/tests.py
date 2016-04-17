from django.test import TestCase
from blog.views import home_page, about_page, new_post_page
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from blog.models import BlogPost

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        resolved_view = resolve("/")
        self.assertEqual(resolved_view.func, home_page)


    def test_home_page_view_uses_home_page_template(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertEqual(response.content.decode(), expected_html)



class AboutPageTest(TestCase):

    def test_about_url_resolves_to_about_view(self):
        resolved_view = resolve("/about/")
        self.assertEqual(resolved_view.func, about_page)


    def test_home_page_view_uses_home_page_template(self):
        request = HttpRequest()
        response = about_page(request)
        expected_html = render_to_string("about.html")
        self.assertEqual(response.content.decode(), expected_html)



class NewBlogPostTest(TestCase):

    def test_new_url_resolves_to_new_view(self):
        resolved_view = resolve("/blog/new/")
        self.assertEqual(resolved_view.func, new_post_page)


    def test_new_post_view_uses_new_post_template(self):
        request = HttpRequest()
        response = new_post_page(request)
        expected_html = render_to_string("new_post.html")
        self.assertEqual(response.content.decode(), expected_html)


    def test_new_post_view_can_save_blog_post(self):
        self.client.post(
         "/blog/new",
         data={
          "title": "Title",
          "date": "1962-10-10",
          "body": "Some text",
          "visible": "yes"
         }
        )
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, "Title")
