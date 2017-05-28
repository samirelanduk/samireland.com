from samireland.tests import ViewTest

class NewBlogPageViewTests(ViewTest):

    def test_new_blog_view_uses_new_blog_template(self):
        response = self.client.get("/blog/new/")
        self.assertTemplateUsed(response, "new-blog.html")
