from datetime import datetime
from samireland.tests import ViewTest

class NewBlogPageViewTests(ViewTest):

    def test_new_blog_view_uses_new_blog_template(self):
        response = self.client.get("/blog/new/")
        self.assertTemplateUsed(response, "new-blog.html")


    def test_new_blog_view_sends_todays_date(self):
        today = datetime.now()
        response = self.client.get("/blog/new/")
        self.assertEqual(response.context["today"], today.strftime("%Y-%m-%d"))


    def test_new_blog_view_redirects_to_blog_page_on_post(self):
        response = self.client.post("/blog/new/")
        self.assertRedirects(response, "/blog/")



class BlogPageViewTests(ViewTest):

    def test_blog_view_uses_blog_template(self):
        response = self.client.get("/blog/")
        self.assertTemplateUsed(response, "blog.html")
