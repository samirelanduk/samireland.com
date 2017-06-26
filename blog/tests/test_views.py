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


    def test_can_handle_missing_date(self):
        response = self.client.post("/blog/new/", data={
         "date": "", "title": "T", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "new-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no date")


    def test_can_handle_duplicate_date(self):
        BlogPost.objects.create(
         date=datetime(2001, 9, 11).date(), title="T", body="B", visible=True
        )
        response = self.client.post("/blog/new/", data={
         "date": "2001-09-11", "title": "TT", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "new-blog.html")
        self.assertEqual(response.context["error"], "There is already a post with that date")


    def test_can_handle_missing_title(self):
        response = self.client.post("/blog/new/", data={
         "date": "2001-09-11", "title": "", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "new-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no title")


    def test_can_handle_missing_body(self):
        response = self.client.post("/blog/new/", data={
         "date": "2001-09-11", "title": "T", "body": "", "visible": "on"
        })
        self.assertTemplateUsed(response, "new-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no body")



class BlogPageViewTests(ViewTest):

    def test_blog_view_uses_blog_template(self):
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "blog.html")


    def test_blog_view_sends_blog_posts(self):
        for d in range(1, 25):
            BlogPost.objects.create(
             date="1990-09-{}".format(25 - d), title="t", body="b", visible=True
            )
        response = self.client.get("/blog/")
        self.assertEqual(
         response.context["posts"],
         [post for post in BlogPost.objects.all()]
        )


    def test_blog_view_sends_posts_in_date_order(self):
        BlogPost.objects.create(
         date="1990-09-2", title="t", body="b", visible=True
        )
        BlogPost.objects.create(
         date="1990-09-1", title="t", body="b", visible=True
        )
        BlogPost.objects.create(
         date="1990-09-3", title="t", body="b", visible=True
        )
        response = self.client.get("/blog/")
        self.assertEqual(response.context["posts"][0].date.day, 3)
        self.assertEqual(response.context["posts"][1].date.day, 2)
        self.assertEqual(response.context["posts"][2].date.day, 1)
