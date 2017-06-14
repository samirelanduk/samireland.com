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

    @patch("samdown.html_from_markdown")
    def test_blog_post_has_samdown_property(self, mock_converter):
        mock_converter.return_value = "test output"
        blog = BlogPost()
        blog.title = "Title"
        blog.body = "Body"
        self.assertEqual(blog.samdown_body, "test output")
        mock_converter.assert_called_with("Body")
