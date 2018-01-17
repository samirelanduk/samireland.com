import os
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, Mock, MagicMock
from seleniumx import TestCaseX
from django.test import TestCase
from samireland.models import *
from samireland.settings import MEDIA_ROOT

class EditableTextTests(TestCase, TestCaseX):

    def test_can_create_editable_text(self):
        text = EditableText(name="home", body="1\n\n2")
        text.full_clean()


    def test_body_is_required(self):
        text = EditableText(name="home")
        with self.assertRaises(ValidationError):
            text.full_clean()


    @patch("docupy.markdown_to_html")
    def test_editable_text_has_markdown_property(self, mock_html):
        mock_html.return_value = "test output"
        text = EditableText(name="home", body="1\n\n2")
        output = text.html
        mock_html.assert_called_with("1\n\n2")
        self.assertEqual(output, "test output")



class PublicationTests(TestCase, TestCaseX):

    def test_can_create_publication(self):
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", doi="12.34", authors="S, B", body="1\n\n2"
        )
        pub.full_clean()


    def test_title_is_required(self):
        pub = Publication(
         id="paper-1", date="2017-01-02",
         url="12/34", doi="12.34", authors="S, B", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    def test_date_is_required(self):
        pub = Publication(
         id="paper-1", title="PT",
         url="12/34", doi="12.34", authors="S, B", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    def test_url_is_required(self):
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         doi="12.34", authors="S, B", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    def test_doi_is_required(self):
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", authors="S, B", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    def test_authors_is_required(self):
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", doi="12.34", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    def test_body_is_required(self):
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", doi="12.34", authors="S, B"
        )
        with self.assertRaises(ValidationError):
            pub.full_clean()


    @patch("docupy.markdown_to_html")
    def test_publication_has_markdown_property(self, mock_html):
        mock_html.return_value = "test output"
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", doi="12.34", authors="S, B", body="1\n\n2"
        )
        output = pub.html
        mock_html.assert_called_with("1\n\n2")
        self.assertEqual(output, "test output")


    @patch("docupy.markdown_to_html")
    def test_publication_has_markdown_authors_property(self, mock_html):
        mock_html.return_value = "test output"
        pub = Publication(
         id="paper-1", title="PT", date="2017-01-02",
         url="12/34", doi="12.34", authors="S, B", body="1\n\n2"
        )
        output = pub.html_authors
        mock_html.assert_called_with("S, B")
        self.assertEqual(output, "test output")



class ProjectTests(TestCase, TestCaseX):

    def test_can_create_project(self):
        project = Project(
         name="palladium", image="palladium-icon", description="1\n\n2",
         category="python"
        )
        project.full_clean()


    def test_project_name_is_required(self):
        project = Project(
         image="palladium-icon", description="1\n\n2", category="python"
        )
        with self.assertRaises(ValidationError):
            project.full_clean()


    def test_project_image_is_required(self):
        project = Project(
         name="palladium", description="1\n\n2", category="python"
        )
        with self.assertRaises(ValidationError):
            project.full_clean()


    def test_project_description_is_required(self):
        project = Project(
         name="palladium", image="palladium-icon", category="python"
        )
        with self.assertRaises(ValidationError):
            project.full_clean()


    def test_project_category_default(self):
        project = Project(
         name="palladium", image="palladium-icon", description="1\n\n2",
        )
        self.assertEqual(project.category, "web")


    @patch("samireland.models.MediaFile.objects.get")
    def test_project_image_fetching(self, mock_get):
        project = Project(
         name="palladium", image="palladium-icon", description="1\n\n2",
         category="python"
        )
        image = Mock()
        image.mediafile = Mock()
        image.mediafile.url = "URL"
        mock_get.return_value = image
        self.assertEqual(project.image_url, "URL")
        mock_get.assert_called_with(name="palladium-icon")


    @patch("samireland.models.MediaFile.objects.get")
    def test_project_image_fetching_no_image(self, mock_get):
        project = Project(
         name="palladium", image="palladium-icon", description="1\n\n2",
         category="python"
        )
        mock_get.side_effect = MediaFile.DoesNotExist
        self.assertEqual(project.image_url, "")
        mock_get.assert_called_with(name="palladium-icon")


    @patch("docupy.markdown_to_html")
    def test_project_has_markdown_property(self, mock_html):
        mock_html.return_value = "test output"
        project = Project(
         name="palladium", image="palladium-icon", description="1\n\n2",
         category="python"
        )
        output = project.html
        mock_html.assert_called_with("1\n\n2")
        self.assertEqual(output, "test output")



class ArticleTests(TestCase, TestCaseX):

    def test_can_create_article(self):
        article = Article(
         id="article-1", title="PT", date="2017-01-02", summary="S", body="1\n\n2"
        )
        article.full_clean()


    def test_title_is_required(self):
        article = Article(
         id="article-1", date="2017-01-02", summary="S", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            article.full_clean()


    def test_date_is_required(self):
        article = Article(
         id="article-1", title="PT", summary="S", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            article.full_clean()


    def test_summary_is_required(self):
        article = Article(
         id="article-1", title="PT", date="2017-01-02", body="1\n\n2"
        )
        with self.assertRaises(ValidationError):
            article.full_clean()


    def test_body_is_required(self):
        article = Article(
         id="article-1", title="PT", date="2017-01-02", summary="S"
        )
        with self.assertRaises(ValidationError):
            article.full_clean()


    @patch("docupy.markdown_to_html")
    def test_article_has_markdown_property(self, mock_html):
        mock_html.return_value = "test output"
        article = Article(
         id="article-1", title="PT", date="2017-01-02", body="1\n\n2"
        )
        output = article.html
        mock_html.assert_called_with("1\n\n2")
        self.assertEqual(output, "test output")



class BlogPostTests(TestCase, TestCaseX):

    def test_can_create_blog_post(self):
        post = BlogPost(date="2017-01-02", title="PT", body="1\n\n2")
        post.full_clean()


    def test_date_is_required(self):
        post = BlogPost(title="PT", body="1\n\n2")
        with self.assertRaises(ValidationError):
            post.full_clean()


    def test_title_is_required(self):
        post = BlogPost(date="2017-01-02", body="1\n\n2")
        with self.assertRaises(ValidationError):
            post.full_clean()


    def test_body_is_required(self):
        post = BlogPost(date="2017-01-02", title="PT")
        with self.assertRaises(ValidationError):
            post.full_clean()


    @patch("docupy.markdown_to_html")
    def test_article_has_markdown_property(self, mock_html):
        mock_html.return_value = "test output"
        post = BlogPost(date="2017-01-02", title="PT", body="1\n\n2")
        output = post.html
        mock_html.assert_called_with("1\n\n2")
        self.assertEqual(output, "test output")



class MediaFileTests(TestCase, TestCaseX):

    def setUp(self):
        self.files_at_start = os.listdir(MEDIA_ROOT)


    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass


    def test_can_generate_filename(self):
        instance = Mock()
        name = MediaFile.create_filename(instance, "filename.bmp")
        self.assertEqual(name[-4:], ".bmp")
        datetime.strptime(name[:-4], "%Y%m%d-%H%M%S")


    def test_can_create_media_files(self):
        self.assertNotIn("123456.png", os.listdir(MEDIA_ROOT))
        media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")
        image = MediaFile(name="test", mediafile=media_file)
        image.full_clean()
        image.save()
        self.assertIn(
         datetime.now().strftime("%Y%m%d-%H%M%S") + ".png",
         os.listdir(MEDIA_ROOT)
        )
