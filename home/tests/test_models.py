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

    @patch("docupy.markdown_to_html")
    @patch("home.models.media_url_lookup")
    def test_editable_text_has_markdown_property(self, mock_url, mock_conv):
        mock_conv.return_value = "test output"
        mock_url.return_value = {"url": "lookup"}
        text = EditableText()
        text.name = "testsnippet"
        text.content = "CONTENT"
        output = text.markdown
        mock_url.assert_called_with()
        mock_conv.assert_called_with("CONTENT", {"url": "lookup"})
