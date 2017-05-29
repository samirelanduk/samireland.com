from datetime import datetime
from django.core.exceptions import ValidationError
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
