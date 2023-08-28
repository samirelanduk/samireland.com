from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class WritingPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
    ]

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "articles": [{
                "title": article.title,
                "date": article.date,
                "slug": article.slug,
                "intro": article.intro,
                "image": article.image.file.url,
                "tags": [{"name": tag.name, "color": tag.color} for tag in article.tags.all()],
            } for article in ArticlePage.objects.all().order_by("-date")]
        })




class ArticlePage(Page):

    date = models.DateField("Article date")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    intro = models.TextField()
    body = StreamField([
        ("text", blocks.RichTextBlock(features=["bold", "link", "italic", "h2", "h3", "ol", "ul", "code", "strikethrough"])),
        ("figure", blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.RichTextBlock(features=["bold", "link", "italic"])),
        ], icon="image")),
        ("code", blocks.StructBlock([
            ("language", blocks.CharBlock()),
            ("code", blocks.TextBlock()),
        ], icon="code")),
    ], use_json_field=True)
    tags = models.ManyToManyField("articles.ArticleTag", related_name="articles")

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("image"),
        FieldPanel("intro"),
        FieldPanel("body", ),
        FieldPanel("tags"),
    ]

    def __str__(self):
        return self.title
    

    def serve(self, request, *args, **kwargs):
        blocks = []
        for block in self.body:
            if block.block_type == "text":
                blocks.append({
                    "type": block.block_type,
                    "value": block.render()
                })
            elif block.block_type == "figure":
                blocks.append({
                    "type": block.block_type,
                    "value": {
                        "image": block.value["image"].file.url,
                        "caption": str(block.value["caption"]),
                    }
                })
            elif block.block_type == "code":
                blocks.append({
                    "type": block.block_type,
                    "value": {
                        "language": block.value["language"],
                        "code": block.value["code"],
                    }
                })
        return JsonResponse({
            "title": self.title,
            "date": self.date,
            "body": blocks,
            "tags": [{"name": tag.name, "color": tag.color} for tag in self.tags.all()],
        })



@register_snippet
class ArticleTag(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name