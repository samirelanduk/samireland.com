from django.db import models
from wagtail.models import Page, Orderable, ParentalKey
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel

class ProjectsPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        InlinePanel("projects", label="Projects"),
    ]

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": self.text,
        })



class Project(Orderable):

    name = models.CharField(max_length=100)
    description = models.TextField()
    code_url = models.URLField()
    about_url = models.URLField()
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    page = ParentalKey(ProjectsPage, on_delete=models.CASCADE, related_name="projects")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("code_url"),
        FieldPanel("about_url"),
        FieldPanel("image"),
    ]
