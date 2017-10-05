from unittest.mock import patch
from samireland.tests import ModelTest
from home.models import EditableText

class CreationTests(ModelTest):

    def test_can_save_and_retrieve_editable_text(self):
        self.assertEqual(EditableText.objects.all().count(), 0)
        text = EditableText()
        text.name = "testsnippet"
        text.content = "CONTENT"
        text.save()
        self.assertEqual(EditableText.objects.all().count(), 1)
        retrieved_text = EditableText.objects.first()
        self.assertEqual(retrieved_text, text)



class PropertyTests(ModelTest):

    @patch("django_samdown.html_from_markdown")
    def test_editable_text_has_samdown_property(self, mock_converter):
        mock_converter.return_value = "test output"
        text = EditableText()
        text.name = "testsnippet"
        text.content = "CONTENT"
        output = text.samdown_content
        mock_converter.assert_called_with("CONTENT")
        self.assertEqual(text.samdown_content, "test output")
