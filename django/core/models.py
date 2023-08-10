from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

class HomePage(Page):

    about = models.TextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("about"),
    ]