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
