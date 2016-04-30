from django.test import TestCase
import samdown

class PostSplittingTests(TestCase):

    def test_one_block_returns_one_block(self):
        self.assertEqual(
         samdown.split("This is a paragraph"),
         ["This is a paragraph"]
        )


    def test_single_new_line_does_not_split(self):
        self.assertEqual(
         samdown.split("This is a paragraph\nThis is the same paragraph"),
         ["This is a paragraph\nThis is the same paragraph"]
        )


    def test_can_split(self):
        self.assertEqual(
         samdown.split("This is a paragraph\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )


    def test_multi_new_lines_ignored(self):
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a paragraph\n\n\n\n\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
        self.assertEqual(
         samdown.split("This is a   paragraph\n\n\nThis is a new paragraph\n\n\nAnd a third"),
         ["This is a   paragraph", "This is a new paragraph", "And a third"]
        )


    def test_windows_new_lines_work(self):
        self.assertEqual(
         samdown.split("This is a paragraph\r\n\r\nThis is a new paragraph"),
         ["This is a paragraph", "This is a new paragraph"]
        )
