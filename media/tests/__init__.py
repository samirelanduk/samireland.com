import os
import datetime
from django.test import TestCase
from samireland.settings import MEDIA_ROOT

class MediaTest(TestCase):

    def tearDown(self):
        try:
            os.remove(MEDIA_ROOT + (
             "/images/%s.png" % datetime.datetime.now().strftime("%Y%m%d")
            ))
        except OSError:
            pass
