from django.db import models
from django.http import JsonResponse
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from core.hooks import *

class HomePage(Page):

    about = models.TextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("about"),
    ]

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "about": self.about,
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })