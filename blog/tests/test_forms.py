from django.test import TestCase
from blog.forms import BlogPostForm

class FormsTest(TestCase):

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
