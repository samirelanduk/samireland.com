from django.db import models
from django.core.validators import RegexValidator
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from django.conf import settings
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, ClusterableModel
from modelcluster.fields import ParentalKey

class AboutPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        InlinePanel("events", label="Events")
    ]

    max_count = 1

    subpage_types = []

    preview_modes = []

    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/about"
    

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "events": [{
                "name": event.name,
                "start": event.start,
                "end": event.end,
                "description": str(RichText(event.description)),
                "image": event.image.file.url if event.image else None,
                "subevents": [{
                    "name": subevent.name,
                    "start": subevent.start,
                    "end": subevent.end,
                    "description": str(RichText(subevent.description)),
                    "image": subevent.image.file.url if subevent.image else None,
                } for subevent in event.subevents.all()],
            } for event in self.events.all()],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



class EventBase(models.Model):

    class Meta:
        abstract = True
    
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=7, validators=[
        RegexValidator(
            regex="\d\d\d\d-\d\d",
            message="Must be in the format YYYY=MM",
        ),
    ])
    end = models.CharField(max_length=7, blank=True, validators=[
        RegexValidator(
            regex="\d\d\d\d-\d\d",
            message="Must be in the format YYYY=MM",
        ),
    ])
    description = RichTextField(blank=True, max_length=1000)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")



class Event(Orderable, ClusterableModel, EventBase):
    
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="events")

    panels = [
        FieldPanel("name"),
        FieldPanel("start"),
        FieldPanel("end"),
        FieldPanel("description"),
        FieldPanel("image"),
        InlinePanel("subevents", label="Subevents")
    ]



class SubEvent(Orderable, EventBase):
    
    event = ParentalKey(Event, on_delete=models.CASCADE, related_name="subevents")

    panels = [
        FieldPanel("name"),
        FieldPanel("start"),
        FieldPanel("end"),
        FieldPanel("image"),
        FieldPanel("description"),
    ]
