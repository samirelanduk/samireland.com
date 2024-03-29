from django.db import models
from wagtail.models import Page, Orderable, ParentalKey
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from django.conf import settings
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet

class ProjectsPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
        InlinePanel("projects", label="Projects"),
    ]

    max_count = 1

    subpage_types = []

    preview_modes = []

    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/projects"

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "projects": [{
                "name": project.name,
                "featured_overview": project.featured_overview,
                "description": project.description,
                "code_url": project.code_url,
                "about_url": project.about_url,
                "image": project.image.file.url,
                "tags": [{"name": tag.name, "color": tag.color} for tag in project.tags.all()],
            } for project in self.projects.all()],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



class Project(Orderable, ClusterableModel):

    name = models.CharField(max_length=100)
    featured_overview = RichTextField(blank=True, max_length=1000)
    description = RichTextField()
    code_url = models.URLField(blank=True, null=True)
    about_url = models.URLField(blank=True, null=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    tags = ParentalManyToManyField("projects.ProjectTag", related_name="projects")
    page = ParentalKey(ProjectsPage, on_delete=models.CASCADE, related_name="projects")

    panels = [
        FieldPanel("name"),
        FieldPanel("featured_overview"),
        FieldPanel("description"),
        FieldPanel("code_url"),
        FieldPanel("about_url"),
        FieldPanel("image"),
        FieldPanel("tags"),
    ]

    def __repr__(self):
        return self.name


    def __str__(self):
        return self.name
    
    @property
    def label(self):
        return self.name



@register_snippet
class ProjectTag(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name
