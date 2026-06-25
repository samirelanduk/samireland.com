from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from django.conf import settings
from wagtail.admin.panels import FieldPanel

class ReadingPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
    ]

    preview_modes = []

    max_count = 1

    subpage_types = []

    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/reading"

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })