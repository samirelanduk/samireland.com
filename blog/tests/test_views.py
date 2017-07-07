from datetime import datetime
from samireland.tests import ViewTest
from django.http import HttpRequest
from blog.models import BlogPost
from blog.processors import years_processor

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


    def test_blog_view_does_send_invisible_posts_when_logged_in(self):
        self.client.login(username="testsam", password="testpassword")
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
        self.assertEqual(len(response.context["posts"]), 3)
        self.assertEqual(response.context["posts"][0].date.day, 3)
        self.assertEqual(response.context["posts"][1].date.day, 2)
        self.assertEqual(response.context["posts"][2].date.day, 1)



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



class BlogPageyearViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        BlogPost.objects.create(
         date="1996-04-28", title="Previous", body="PPP", visible=True
        )
        BlogPost.objects.create(
         date="1997-05-1", title="Win", body="TB Wins", visible=True
        )
        BlogPost.objects.create(
         date="1997-05-5", title="Next", body="NNN", visible=True
        )
        BlogPost.objects.create(
         date="1998-05-5", title="Next Next", body="NNN", visible=True
        )


    def test_blog_year_view_uses_blog_year_template(self):
        response = self.client.get("/blog/1997/")
        self.assertTemplateUsed(response, "year-posts.html")


    def test_blog_year_view_returns_404_if_no_post(self):
        response = self.client.get("/blog/1992/")
        self.assertEqual(response.status_code, 404)


    def test_blog_year_view_sends_year(self):
        response = self.client.get("/blog/1997/")
        self.assertEqual(response.context["year"], 1997)


    def test_blog_year_view_returns_404_if_invisible_post(self):
        BlogPost.objects.create(
         date="1993-04-30", title="Shhh", body="PPP", visible=False
        )
        response = self.client.get("/blog/1993/")
        self.assertEqual(response.status_code, 404)


    def test_blog_year_view_sends_blog_posts(self):
        response = self.client.get("/blog/1997/")
        self.assertEqual(
         response.context["posts"], [
          BlogPost.objects.filter(title="Next").first(),
          BlogPost.objects.filter(title="Win").first()
         ]
        )


    def test_blog_year_view_does_not_send_invisible_posts(self):
        BlogPost.objects.create(
         date="1997-06-5", title="Sh", body="NNN", visible=False
        )
        response = self.client.get("/blog/1997/")
        self.assertEqual(len(response.context["posts"]), 2)
        self.assertEqual(response.context["posts"][0].date.day, 5)
        self.assertEqual(response.context["posts"][1].date.day, 1)


    def test_blog_year_view_sends_surrounding_years(self):
        response = self.client.get("/blog/1997/")
        self.assertEqual(response.context["previous"], 1996)
        self.assertEqual(response.context["next"], 1998)


    def test_one_post_view_sends_surrounding_posts_at_edges(self):
        response = self.client.get("/blog/1998/")
        self.assertEqual(response.context["previous"], 1997)
        self.assertEqual(response.context["next"], None)
        response = self.client.get("/blog/1996/")
        self.assertEqual(response.context["previous"], None)
        self.assertEqual(response.context["next"], 1997)


    def test_surrounding_posts_ignores_invisible_posts(self):
        BlogPost.objects.create(
         date="1999-04-30", title="Shhh", body="PPP", visible=False
        )
        response = self.client.get("/blog/1998/")
        self.assertEqual(response.context["previous"], 1997)
        self.assertEqual(response.context["next"], None)



class NewBlogPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        BlogPost.objects.create(
         date="1996-04-28", title="Previous", body="PPP", visible=True
        )


    def test_edit_blog_view_uses_edit_blog_template(self):
        response = self.client.get("/blog/1996/4/28/edit/")
        self.assertTemplateUsed(response, "edit-blog.html")


    def test_edit_blog_view_sends_404_if_no_post(self):
        response = self.client.get("/blog/1986/4/28/edit/")
        self.assertEqual(response.status_code, 404)


    def test_edit_blog_view_sends_post(self):
        response = self.client.get("/blog/1996/4/28/edit/")
        self.assertEqual(response.context["post"], BlogPost.objects.first())


    def test_edit_blog_view_redirects_to_post_page_on_post(self):
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1990-09-28", "title": "T", "body": "BBB", "visible":True
        })
        self.assertRedirects(response, "/blog/1990/9/28/")


    def test_edit_blog_view_redirects_to_blog_page_on_post_if_invisible(self):
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1990-09-28", "title": "T", "body": "BBB"
        })
        self.assertRedirects(response, "/blog/")


    def test_edit_blog_view_edits_posts(self):
        self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1990-09-28", "title": "T", "body": "BBB",
        })
        self.assertEqual(BlogPost.objects.all().count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.date, datetime(1990, 9, 28).date())
        self.assertEqual(post.title, "T")
        self.assertEqual(post.body, "BBB")
        self.assertEqual(post.visible, False)


    def test_can_handle_missing_date(self):
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "", "title": "T", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "edit-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no date")


    def test_can_handle_duplicate_date(self):
        BlogPost.objects.create(
         date=datetime(2001, 9, 11).date(), title="T", body="B", visible=True
        )
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "2001-09-11", "title": "TT", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "edit-blog.html")
        self.assertEqual(response.context["error"], "There is already a post with that date")
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1996-04-28", "title": "T", "body": "BBB", "visible": "on"
        })
        self.assertRedirects(response, "/blog/1996/4/28/")


    def test_can_handle_missing_title(self):
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1996-04-28", "title": "", "body": "BBB", "visible": "on"
        })
        self.assertTemplateUsed(response, "edit-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no title")


    def test_can_handle_missing_body(self):
        response = self.client.post("/blog/1996/4/28/edit/", data={
         "date": "1996-04-28", "title": "T", "body": "", "visible": "on"
        })
        self.assertTemplateUsed(response, "edit-blog.html")
        self.assertEqual(response.context["error"], "You cannot submit a post with no body")



class BlogtemplateContextProcessorTests(ViewTest):

    def test_processor_adds_relevant_years(self):
        BlogPost.objects.create(
         date="1997-04-30", title="Shhh", body="PPP", visible=True
        )
        BlogPost.objects.create(
         date="1999-04-30", title="Shhh", body="PPP", visible=True
        )
        request = HttpRequest()
        context = years_processor(request)
        self.assertEqual(context, {"blog_years": [1999, 1997]})


    def test_processor_ignores_invisible_years(self):
        BlogPost.objects.create(
         date="1997-04-30", title="Shhh", body="PPP", visible=True
        )
        BlogPost.objects.create(
         date="1998-04-30", title="Shhh", body="PPP", visible=False
        )
        BlogPost.objects.create(
         date="1999-04-30", title="Shhh", body="PPP", visible=True
        )
        request = HttpRequest()
        context = years_processor(request)
        self.assertEqual(context, {"blog_years": [1999, 1997]})
