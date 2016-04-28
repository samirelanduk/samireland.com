from django.test import TestCase
from blog import views
from blog.forms import BlogPostForm
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


    def test_edits_url_resolves_to_edits_post(self):
        self.check_url_returns_view("/blog/edit/", views.edit_posts_page)


    def test_edit_url_resolves_to_edit_post(self):
        self.check_url_returns_view("/blog/edit/100/", views.edit_post_page)


    def test_delete_url_resolves_to_delete_post(self):
        self.check_url_returns_view("/blog/delete/100/", views.delete_post_page)



class ModelTests(TestCase):

    def test_save_and_retrieve_blog_posts(self):
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


    def test_cannot_create_post_without_title(self):
        blog_post = BlogPost(title="", date=datetime.datetime.now(), body=".", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.save()
            blog_post.full_clean()


    def test_cannot_create_post_without_date(self):
        blog_post = BlogPost(title=".", date="", body=".", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.save()
            blog_post.full_clean()


    def test_cannot_create_post_without_body(self):
        blog_post = BlogPost(title="", date=datetime.datetime.now(), body="", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.save()
            blog_post.full_clean()



class FormsTest(TestCase):

    def test_blog_form_has_correct_inputs(self):
        form = BlogPostForm()
        self.assertIn(
         '<input id="id_title" name="title" type="text"',
         str(form)
        )
        self.assertIn(
         '<input id="id_date" name="date" type="date"',
         str(form)
        )
        self.assertIn(
         '<textarea id="id_body" name="body"',
         str(form)
        )
        self.assertIn(
         '<input id="id_visible" name="visible" type="checkbox"',
         str(form)
        )


    def test_blog_form_wont_accept_blank_title(self):
        form = BlogPostForm(data={
         "title": "",
         "date": "1939-09-01",
         "body": ".",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["title"],
         ["You cannot submit a blog post with no title"]
        )


    def test_blog_form_wont_accept_blank_date(self):
        form = BlogPostForm(data={
         "title": ".",
         "date": "",
         "body": ".",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["date"],
         ["You cannot submit a blog post with no date"]
        )


    def test_blog_form_wont_accept_blank_body(self):
        form = BlogPostForm(data={
         "title": ".",
         "date": "1939-09-01",
         "body": "",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["body"],
         ["You cannot submit a blog post with no body"]
        )




class ViewTests(TestCase):

    def check_view_uses_template(self, view, template, *view_args, template_dict=None):
        template_dict = template_dict if template_dict else {}
        request = HttpRequest()
        response = view(request, *view_args)
        expected_html = render_to_string(template, template_dict)
        self.maxDiff = None
        self.assertEqual(response.content.decode(), expected_html)


    def make_post_request(self, title=".", date="1939-09-01", body=".", visible=True):
        request = HttpRequest()
        request.method = "POST"
        request.POST["title"] = title
        request.POST["date"] = date
        request.POST["body"] = body
        request.POST["visible"] = visible
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
        request = HttpRequest()
        return view(request).content.decode()


    def save_test_post_to_db(self):
        post = BlogPost(
         date=datetime.datetime(1900, 1, 1).date(),
         title="Test title",
         body="Test body",
         visible=True
        )
        post.save()
        return post.id


    def test_home_page_view_uses_home_page_template(self):
        self.check_view_uses_template(views.home_page, "home.html")


    def test_home_view_uses_most_recent_blog_post(self):
        home_html = self.get_html_after_three_blog_posts(views.home_page)
        self.assertIn("1960", home_html)
        self.assertNotIn("1950", home_html)
        self.assertNotIn("1955", home_html)


    def test_home_view_ignores_invisible_posts(self):
        home_html = self.get_html_after_three_blog_posts(
         views.home_page, last_invisible=True
        )
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
        blog_html = self.get_html_after_three_blog_posts(
         views.blog_page, last_invisible=True
        )
        pos_1950 = blog_html.find("January, 1950")
        pos_1955 = blog_html.find("January, 1955")
        pos_1960 = blog_html.find("January, 1960")
        self.assertTrue(pos_1955 < pos_1950)
        self.assertEqual(pos_1960, -1)


    def test_new_post_view_uses_new_post_template(self):
        form = BlogPostForm()
        self.check_view_uses_template(
         views.new_post_page,
         "new_post.html",
         template_dict={"form": form}
        )


    def test_new_post_view_uses_blog_post_form(self):
        request = HttpRequest()
        response = views.new_post_page(request)
        self.assertIn(
         BlogPostForm().__dict__["fields"]["title"].widget.render(
          name="title",
          value="",
          attrs={"id": "id_title"}
         ),
         response.content.decode()
        )


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


    def test_new_post_page_returns_error_message_when_needed(self):
        request = self.make_post_request(title="")
        response = views.new_post_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cannot submit", response.content.decode())


    def test_new_post_view_does_not_save_to_db_after_error(self):
        self.assertEqual(BlogPost.objects.count(), 0)
        request = self.make_post_request(title="")
        response = views.new_post_page(request)
        self.assertEqual(BlogPost.objects.count(), 0)


    def test_new_post_vew_can_recover_from_empty_date(self):
        request = self.make_post_request(date="")
        response = views.new_post_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cannot submit", response.content.decode())


    def test_edit_posts_view_uses_edit_posts_template(self):
        self.check_view_uses_template(views.edit_posts_page, "edit_posts.html")


    def test_edit_posts_view_shows_all_posts_in_correct_order(self):
        html = self.get_html_after_three_blog_posts(
         views.edit_posts_page, last_invisible=True
        )
        pos_1950 = html.find("January, 1950")
        pos_1955 = html.find("January, 1955")
        pos_1960 = html.find("January, 1960")
        self.assertTrue(pos_1960 < pos_1955 < pos_1950)


    def test_edit_post_view_uses_edit_post_template(self):
        post_id = self.save_test_post_to_db()
        blog_post = BlogPost.objects.first()
        form = BlogPostForm(instance=blog_post)
        self.check_view_uses_template(
         views.edit_post_page,
         "edit_post.html",
         post_id,
         template_dict={"form": form, "id": post_id}
        )


    def test_edit_post_view_uses_blog_post_form(self):
        post_id = self.save_test_post_to_db()
        request = HttpRequest()
        response = views.edit_post_page(request, post_id)
        self.assertIn(
         BlogPostForm().__dict__["fields"]["title"].widget.render(
          name="title",
          value="Test title",
          attrs={"id": "id_title"}
         ),
         response.content.decode()
        )


    def test_edit_post_view_contains_post_text(self):
        post_id = self.save_test_post_to_db()
        request = HttpRequest()
        html = views.edit_post_page(request, post_id).content.decode()
        self.assertIn("Test title", html)
        self.assertIn("1900-01-01", html)
        self.assertIn("Test body", html)
        self.assertIn("checked", html)


    def test_edit_post_view_redirects_after_post(self):
        request = self.make_post_request()
        post_id = self.save_test_post_to_db()
        response = views.edit_post_page(request, post_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/blog/")


    def test_edit_post_page_can_actually_edit_a_post(self):
        request = self.make_post_request()
        post_id = self.save_test_post_to_db()
        post = BlogPost.objects.first()
        self.assertEqual(post.title, "Test title")
        response = views.edit_post_page(request, post_id)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, ".")


    def test_edit_post_page_returns_error_message_when_needed(self):
        post_id = self.save_test_post_to_db()
        request = self.make_post_request(title="")
        response = views.edit_post_page(request, post_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cannot submit", response.content.decode())


    def test_edit_post_view_does_not_save_to_db_after_error(self):
        post_id = self.save_test_post_to_db()
        request = self.make_post_request(title="")
        response = views.edit_post_page(request, post_id)
        self.assertEqual(BlogPost.objects.first().title, "Test title")


    def test_edit_post_vew_can_recover_from_empty_date(self):
        post_id = self.save_test_post_to_db()
        request = self.make_post_request(date="")
        response = views.edit_post_page(request, post_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("cannot submit", response.content.decode())


    def test_delete_post_view_redirects_after_post(self):
        request = self.make_post_request()
        post_id = self.save_test_post_to_db()
        response = views.delete_post_page(request, post_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/blog/edit/")


    def test_delete_post_can_actually_delete_a_post(self):
        post_id = self.save_test_post_to_db()
        self.assertEqual(BlogPost.objects.count(), 1)
        request = HttpRequest()
        request.method = "POST"
        views.delete_post_page(request, post_id)
        self.assertEqual(BlogPost.objects.count(), 0)
