import datetime
from django.test import TestCase
from blog import views
from blog.models import BlogPost
from blog.forms import BlogPostForm

class ViewTest(TestCase):

    def create_blog_post(self, title=".", date=datetime.datetime.now().date(),
     body="...", visible=True):
        blog_post = BlogPost.objects.create(
         title=title,
         date=date,
         body=body,
         visible=visible
        )
        return blog_post


    def post_blog_post_to_view(self, view_url, title=".", date="1990-09-28", body="...",
     visible=False):
        response = self.client.post(view_url, data={
         "title": title,
         "date": date,
         "body": body,
         "visible": visible
        })
        return response



class HomePageViewTests(ViewTest):

    def test_home_page_view_uses_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


    def test_home_page_view_shows_most_recent_blog_post(self):
        self.create_blog_post(date=datetime.datetime(1990, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1992, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1991, 9, 28).date())
        response = self.client.get("/")
        self.assertContains(response, "1992")
        self.assertNotContains(response, "1991")
        self.assertNotContains(response, "1990")


    def test_home_page_view_ignores_inivisble_blog_posts(self):
        self.create_blog_post(date=datetime.datetime(1990, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1992, 9, 28).date(), visible=False)
        self.create_blog_post(date=datetime.datetime(1991, 9, 28).date())
        response = self.client.get("/")
        self.assertContains(response, "1991")
        self.assertNotContains(response, "1992")
        self.assertNotContains(response, "1990")



class AboutPageViewTests(ViewTest):

    def test_about_page_view_uses_about_page_template(self):
        response = self.client.get("/about/")
        self.assertTemplateUsed(response, "about.html")



class BlogPageViewTests(ViewTest):

    def test_blog_page_view_uses_blog_page_template(self):
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "blog.html")


    def test_blog_page_shows_posts_in_correct_order(self):
        self.create_blog_post(date=datetime.datetime(1990, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1992, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1991, 9, 28).date())
        response = self.client.get("/blog/")
        pos_1990 = response.content.decode().find("September, 1990")
        pos_1991 = response.content.decode().find("September, 1991")
        pos_1992 = response.content.decode().find("September, 1992")
        self.assertTrue(pos_1992 < pos_1991 < pos_1990)


    def test_blog_page_ignores_invisible_posts(self):
        self.create_blog_post(date=datetime.datetime(1990, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1992, 9, 28).date(), visible=False)
        self.create_blog_post(date=datetime.datetime(1991, 9, 28).date())
        response = self.client.get("/blog/")
        pos_1990 = response.content.decode().find("September, 1990")
        pos_1991 = response.content.decode().find("September, 1991")
        pos_1992 = response.content.decode().find("September, 1992")
        self.assertTrue(pos_1991 < pos_1990)
        self.assertEqual(pos_1992, -1)



class NewBlogPostViewTests(ViewTest):

    def test_new_blog_post_view_uses_new_blog_post_template(self):
        response = self.client.get("/blog/new/")
        self.assertTemplateUsed(response, "new_post.html")


    def test_new_blog_post_view_uses_new_blog_post_form(self):
        response = self.client.get("/blog/new/")
        self.assertIsInstance(response.context["form"], BlogPostForm)


    def test_new_blog_post_view_can_save_blog_posts(self):
        self.assertEqual(BlogPost.objects.count(), 0)
        self.post_blog_post_to_view("/blog/new/")
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, ".")
        self.assertEqual(blog_post.date, datetime.datetime(1990, 9, 28).date())
        self.assertEqual(blog_post.body, "...")
        self.assertEqual(blog_post.visible, False)


    def test_new_blog_post_view_redirects_after_POST(self):
        response = self.post_blog_post_to_view("/blog/new/")
        self.assertRedirects(response, "/")


    def test_new_blog_post_view_returns_error_message_when_needed(self):
        response = self.post_blog_post_to_view("/blog/new/", title="")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot submit")


    def test_new_blog_post_view_does_not_save_to_db_after_error(self):
        self.assertEqual(BlogPost.objects.count(), 0)
        self.post_blog_post_to_view("/blog/new/", title="")
        self.assertEqual(BlogPost.objects.count(), 0)



class EditBlogPostsViewTests(ViewTest):

    def test_edit_blog_posts_view_uses_edit_blog_posts_template(self):
        response = self.client.get("/blog/edit/")
        self.assertTemplateUsed(response, "edit_posts.html")


    def test_edit_blog_posts_view_shows_all_posts_in_correct_order(self):
        self.create_blog_post(date=datetime.datetime(1990, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1992, 9, 28).date())
        self.create_blog_post(date=datetime.datetime(1991, 9, 28).date())
        response = self.client.get("/blog/edit/")
        pos_1990 = response.content.decode().find("September, 1990")
        pos_1991 = response.content.decode().find("September, 1991")
        pos_1992 = response.content.decode().find("September, 1992")
        self.assertTrue(pos_1992 < pos_1991 < pos_1990)



class EditBlogPostViewTests(ViewTest):

    def test_edit_blog_post_view_uses_edit_blog_post_template(self):
        blog_post = self.create_blog_post()
        response = self.client.get("/blog/edit/%i/" % blog_post.id)
        self.assertTemplateUsed(response, "edit_post.html")


    def test_edit_blog_post_view_uses_edit_blog_post_form(self):
        blog_post = self.create_blog_post()
        response = self.client.get("/blog/edit/%i/" % blog_post.id)
        self.assertIsInstance(response.context["form"], BlogPostForm)


    def test_edit_blog_post_view_contains_blog_post_text(self):
        blog_post = self.create_blog_post(title="Titular", body="Bodacious")
        response = self.client.get("/blog/edit/%i/" % blog_post.id)
        self.assertContains(response, "Titular")
        self.assertContains(response, "Bodacious")


    def test_edit_blog_post_view_redirects_after_POST(self):
        blog_post = self.create_blog_post()
        response = self.post_blog_post_to_view("/blog/edit/%i/" % blog_post.id)
        self.assertRedirects(response, "/blog/")


    def test_edit_blog_post_view_can_actually_edit_a_post(self):
        blog_post = self.create_blog_post(title="original")
        self.assertEqual(blog_post.title, "original")
        self.post_blog_post_to_view("/blog/edit/%i/" % blog_post.id, title="new")
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, "new")


    def test_edit_blog_post_view_returns_error_message_when_needed(self):
        blog_post = self.create_blog_post()
        response = self.post_blog_post_to_view("/blog/edit/%i/" % blog_post.id, title="")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot submit")


    def test_edit_blog_post_view_does_not_save_to_db_after_error(self):
        blog_post = self.create_blog_post()
        response = self.post_blog_post_to_view("/blog/edit/%i/" % blog_post.id, title="")
        self.assertEqual(BlogPost.objects.first().title, ".")



class DeleteBlogPostViewTests(ViewTest):

    def test_delete_blog_post_view_uses_delete_blog_post_template(self):
        blog_post = self.create_blog_post()
        response = self.client.get("/blog/delete/%i/" % blog_post.id)
        self.assertTemplateUsed(response, "delete_post.html")


    def test_delete_blog_post_view_redirects_after_POST(self):
        blog_post = self.create_blog_post()
        response = self.post_blog_post_to_view("/blog/delete/%i/" % blog_post.id)
        self.assertRedirects(response, "/blog/edit/")


    def test_delete_blog_post_page_can_actually_delete_a_post(self):
        blog_post = self.create_blog_post()
        self.assertEqual(BlogPost.objects.count(), 1)
        self.client.post("/blog/delete/%i/" % blog_post.id)
        self.assertEqual(BlogPost.objects.count(), 0)
