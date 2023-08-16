from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from wagtail.admin.panels import FieldPanel

class AboutPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
    ]

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
        })