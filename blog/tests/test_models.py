from datetime import datetime
from django.core.exceptions import ValidationError
from unittest.mock import patch
from samireland.tests import ModelTest
from blog.models import BlogPost

class BlogPostTests(ModelTest):

    def test_save_and_retrieve_blog_posts(self):
        self.assertEqual(BlogPost.objects.all().count(), 0)
        post = BlogPost()
        post.date = datetime(1939, 9, 1).date()
        post.title = "War!"
        post.body = "This country is at war."
        post.visible = True
        post.save()
        self.assertEqual(BlogPost.objects.all().count(), 1)
        retrieved_post = BlogPost.objects.first()
        self.assertEqual(retrieved_post, post)


    def test_blog_date_has_to_be_unique(self):
        today = datetime.now().date()
        BlogPost.objects.create(date=today, title="t", body="B", visible=True)
        with self.assertRaises(ValidationError):
            post = BlogPost(date=today, title="tt", body="BN", visible=True)
            post.full_clean()



class PropertyTests(ModelTest):

    @patch("docupy.markdown_to_html")
    @patch("blog.models.media_url_lookup")
    def test_blog_post_has_markdown_property(self, mock_url, mock_conv):
        mock_conv.return_value = "test output"
        mock_url.return_value = {"url": "lookup"}
        blog = BlogPost()
        blog.title = "Title"
        blog.body = "Body"
        output = blog.markdown
        mock_url.assert_called_with()
        mock_conv.assert_called_with("Body", {"url": "lookup"})
