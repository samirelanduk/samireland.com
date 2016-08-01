import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from blog.models import BlogPost

class ModelCreationTest(TestCase):

    def test_save_and_retrieve_blog_posts(self):
        self.assertEqual(BlogPost.objects.all().count(), 0)
        blog_post = BlogPost()
        blog_post.title = "A post"
        blog_post.date = datetime.datetime(1939, 9, 1, 5, 0, 0)
        blog_post.body = "Blah blah blah"
        blog_post.visible = False
        blog_post.save()
        self.assertEqual(BlogPost.objects.all().count(), 1)

        retrieved_post = BlogPost.objects.first()
        self.assertEqual(retrieved_post, blog_post)



class ModelValidationTest(TestCase):

    def test_cannot_create_post_without_title(self):
        blog_post = BlogPost(title="", date=datetime.datetime.now(), body=".", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.full_clean()


    def test_cannot_create_post_without_date(self):
        blog_post = BlogPost(title=".", date="", body=".", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.full_clean()


    def test_cannot_create_post_without_body(self):
        blog_post = BlogPost(title="", date=datetime.datetime.now(), body="", visible=True)
        with self.assertRaises(ValidationError):
            blog_post.full_clean()


    def test_cannot_create_two_posts_with_same_date(self):
        today = datetime.datetime.now().date()
        BlogPost.objects.create(title=".", date=today, body=".", visible=True)
        with self.assertRaises(ValidationError):
            post = BlogPost(title=".", date=today, body=".", visible=True)
            post.full_clean()
