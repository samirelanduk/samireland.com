import os
from django.test import TestCase
from samireland.settings import MEDIA_ROOT

class MediaTest(TestCase):

    def tearDown(self):
        try:
            os.remove(MEDIA_ROOT + "/images/test.png")
        except OSError:
            pass
