from django.db import models
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

    subpage_types = ["reading.QueuePage"]

    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/reading"

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "queue": [{
                "title": queue.title,
                "description": queue.description,
                "slug": queue.slug,
            } for queue in QueuePage.objects.filter(live=True)],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



class QueuePage(Page):

    description = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    parent_page_type = ["reading.ReadingPage"]

    preview_modes = []

    also_revalidate = ["/reading"]


    def __str__(self):
        return self.title


    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/reading/{self.slug}"
    

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "description": self.description,
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })