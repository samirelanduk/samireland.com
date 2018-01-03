from django.core.exceptions import ValidationError, ObjectDoesNotExist
from unittest.mock import patch, Mock, MagicMock
from seleniumx import TestCaseX
from django.test import TestCase
from samireland.models import EditableText

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
