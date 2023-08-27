from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey

class AboutPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        InlinePanel("events", label="Events")
    ]

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "events": [{
                "name": event.name,
                "start": event.start,
                "end": event.end,
                "description": str(RichText(event.description)),
                "image": event.image.file.url if event.image else None
            } for event in self.events.all()]
        })



class Event(Orderable):

    name = models.CharField(max_length=100)
    start = models.CharField(max_length=7)
    end = models.CharField(max_length=7, blank=True)
    description = RichTextField(blank=True, max_length=1000)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="events")
