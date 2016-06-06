import os
import datetime
from django.test import TestCase
from samireland.settings import MEDIA_ROOT

class MediaTest(TestCase):

    def setUp(self):
        self.files_at_start = os.listdir(MEDIA_ROOT)

    def tearDown(self):
        for f in os.listdir(MEDIA_ROOT):
            if f not in self.files_at_start:
                try:
                    os.remove(MEDIA_ROOT + "/" + f)
                except OSError:
                    pass
