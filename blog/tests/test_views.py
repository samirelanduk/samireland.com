from datetime import datetime
from samireland.tests import ViewTest
from blog.models import BlogPost

class NewBlogPageViewTests(ViewTest):

    def test_new_blog_view_uses_new_blog_template(self):
        response = self.client.get("/blog/new/")
        self.assertTemplateUsed(response, "new-blog.html")


    def test_new_blog_view_sends_todays_date(self):
        today = datetime.now()
        response = self.client.get("/blog/new/")
        self.assertEqual(response.context["today"], today.strftime("%Y-%m-%d"))


    def test_new_blog_view_redirects_to_blog_page_on_post(self):
        response = self.client.post("/blog/new/", data={
         "date": "1990-09-28", "title": "T", "body": "BBB", "visible": "on"
        })
        self.assertRedirects(response, "/blog/")


    def test_can_create_blog_post(self):
        self.assertEqual(BlogPost.objects.all().count(), 0)
        self.client.post("/blog/new/", data={
         "date": "1990-09-28", "title": "T", "body": "BBB", "visible": "on"
        })
        self.assertEqual(BlogPost.objects.all().count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.date, datetime(1990, 9, 28).date())
        self.assertEqual(post.title, "T")
        self.assertEqual(post.body, "BBB")
        self.assertEqual(post.visible, True)



class BlogPageViewTests(ViewTest):

    def test_blog_view_uses_blog_template(self):
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "blog.html")


    def test_blog_view_sends_blog_posts(self):
        for d in range(1, 25):
            BlogPost.objects.create(
             date="1990-09-{}".format(d), title="t", body="b", visible=True
            ).save()
        response = self.client.get("/blog/")
        self.assertEqual(
         response.context["posts"],
         [post for post in BlogPost.objects.all()]
        )
