from django.db import models
from wagtail.models import Page, Orderable
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel

class ProjectsPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        InlinePanel("projects", label="Projects"),
    ]



class Project(Orderable):

    name = models.CharField(max_length=100)
    description = models.TextField()
    code_url = models.URLField()
    about_url = models.URLField()
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    page = models.ForeignKey(ProjectsPage, on_delete=models.CASCADE, related_name="projects")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("code_url"),
        FieldPanel("about_url"),
        FieldPanel("image"),
    ]
