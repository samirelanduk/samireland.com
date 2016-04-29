import datetime
from django.test import TestCase
from blog.forms import BlogPostForm
from blog.models import BlogPost

class FormsRenderingTest(TestCase):

    def test_blog_form_has_correct_inputs(self):
        form = BlogPostForm()
        self.assertIn(
         'name="title" type="text"',
         str(form)
        )
        self.assertIn(
         'name="date" type="date"',
         str(form)
        )
        self.assertIn(
         '<textarea',
         str(form)
        )
        self.assertIn(
         'name="body"',
         str(form)
        )
        self.assertIn(
         'name="visible" type="checkbox"',
         str(form)
        )



class FormsValidationTest(TestCase):

    def test_blog_form_wont_accept_blank_title(self):
        form = BlogPostForm(data={
         "title": "",
         "date": "1939-09-01",
         "body": ".",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["title"],
         ["You cannot submit a blog post with no title"]
        )


    def test_blog_form_wont_accept_blank_date(self):
        form = BlogPostForm(data={
         "title": ".",
         "date": "",
         "body": ".",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["date"],
         ["You cannot submit a blog post with no date"]
        )


    def test_blog_form_wont_accept_blank_body(self):
        form = BlogPostForm(data={
         "title": ".",
         "date": "1939-09-01",
         "body": "",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["body"],
         ["You cannot submit a blog post with no body"]
        )


    def test_blog_form_wont_accept_duplicate_dates(self):
        date = datetime.datetime(1990, 9, 28).date()
        BlogPost.objects.create(title=".", date=date, body=".", visible=True)
        form = BlogPostForm(data={
         "title": ".",
         "date": "1990-09-28",
         "body": ".",
         "visible": True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["date"],
         ["There is already a blog post for this date"]
        )
