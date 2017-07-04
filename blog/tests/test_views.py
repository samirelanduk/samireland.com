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
        self.assertEqual(len(response.context["posts"]), 3)
        self.assertEqual(response.context["posts"][0].date.day, 3)
        self.assertEqual(response.context["posts"][1].date.day, 2)
        self.assertEqual(response.context["posts"][2].date.day, 1)


    def test_blog_view_does_not_send_invisible_posts_when_logged_out(self):
        self.client.logout()
        BlogPost.objects.create(
         date="1990-09-2", title="t", body="b", visible=True
        )
        BlogPost.objects.create(
         date="1990-09-1", title="t", body="b", visible=False
        )
        BlogPost.objects.create(
         date="1990-09-3", title="t", body="b", visible=True
        )
        response = self.client.get("/blog/")
        self.assertEqual(len(response.context["posts"]), 2)
        self.assertEqual(response.context["posts"][0].date.day, 3)
        self.assertEqual(response.context["posts"][1].date.day, 2)



class OnePostPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        BlogPost.objects.create(
         date="1997-04-28", title="Previous", body="PPP", visible=True
        )
        BlogPost.objects.create(
         date="1997-05-1", title="Win", body="TB Wins", visible=True
        )
        BlogPost.objects.create(
         date="1997-05-5", title="Next", body="NNN", visible=True
        )


    def test_one_post_view_uses_one_post_template(self):
        response = self.client.get("/blog/1997/5/1/")
        self.assertTemplateUsed(response, "one-post.html")


    def test_one_post_view_returns_404_if_no_post(self):
        response = self.client.get("/blog/1997/5/2/")
        self.assertEqual(response.status_code, 404)


    def test_one_post_view_returns_404_if_invisible_post(self):
        BlogPost.objects.create(
         date="1997-04-30", title="Shhh", body="PPP", visible=False
        )
        response = self.client.get("/blog/1997/4/30/")
        self.assertEqual(response.status_code, 404)


    def test_one_post_view_sends_post(self):
        response = self.client.get("/blog/1997/5/1/")
        self.assertEqual(
         response.context["post"], BlogPost.objects.filter(title="Win").first()
        )


    def test_one_post_view_sends_surrounding_posts(self):
        response = self.client.get("/blog/1997/5/1/")
        self.assertEqual(
         response.context["previous"], BlogPost.objects.filter(title="Previous").first()
        )
        self.assertEqual(
         response.context["next"], BlogPost.objects.filter(title="Next").first()
        )


    def test_surrounding_posts_ignores_invisible_posts(self):
        BlogPost.objects.create(
         date="1997-04-30", title="Shhh", body="PPP", visible=False
        )
        response = self.client.get("/blog/1997/5/1/")
        self.assertEqual(
         response.context["previous"], BlogPost.objects.filter(title="Previous").first()
        )
        self.assertEqual(
         response.context["next"], BlogPost.objects.filter(title="Next").first()
        )


    def test_one_post_view_sends_surrounding_posts_at_edges(self):
        response = self.client.get("/blog/1997/5/5/")
        self.assertEqual(
         response.context["previous"], BlogPost.objects.filter(title="Win").first()
        )
        self.assertEqual(
         response.context["next"], None
        )
        response = self.client.get("/blog/1997/4/28/")
        self.assertEqual(
         response.context["previous"], None
        )
        self.assertEqual(
         response.context["next"], BlogPost.objects.filter(title="Win").first()
        )
