from django.core.exceptions import ValidationError, ObjectDoesNotExist
from unittest.mock import patch, Mock, MagicMock
from seleniumx import TestCaseX
from django.test import TestCase
from samireland.models import EditableText, Publication

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
