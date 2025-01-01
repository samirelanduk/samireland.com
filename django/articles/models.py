from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from django.conf import settings
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail import blocks
from modelcluster.fields import ParentalManyToManyField
from wagtail.images.blocks import ImageChooserBlock

class WritingPage(Page):

    text = RichTextField(blank=True, max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("text"),
    ]

    preview_modes = []

    max_count = 1

    subpage_types = ["articles.ArticlePage"]

    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/writing"

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            "title": self.title,
            "text": str(RichText(self.text)),
            "articles": [{
                "title": article.title,
                "date": article.date,
                "slug": article.slug,
                "intro": article.intro,
                "image": article.image.file.url if article.image else None,
                "tags": [{"name": tag.name, "color": tag.color} for tag in article.tags.all()],
            } for article in ArticlePage.objects.filter(live=True).order_by("-date")],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



class ArticlePage(Page):

    date = models.DateField("Article date")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    intro = models.TextField()
    body = StreamField([
        ("text", blocks.RichTextBlock(features=["bold", "link", "italic", "h2", "h3", "ol", "ul", "code", "strikethrough"])),
        ("figure", blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.RichTextBlock(features=["bold", "link", "italic"], required=False)),
        ], icon="image")),
        ("code", blocks.StructBlock([
            ("language", blocks.CharBlock()),
            ("code", blocks.TextBlock()),
        ], icon="code")),
        ("section", blocks.StructBlock([
            ("title", blocks.CharBlock()),
            ("subtitle", blocks.CharBlock(required=False)),
            ("body", blocks.StreamBlock([
                ("text", blocks.RichTextBlock(features=["bold", "link", "italic", "h2", "h3", "ol", "ul", "code", "strikethrough"])),
                ("figure", blocks.StructBlock([
                    ("image", ImageChooserBlock()),
                    ("caption", blocks.RichTextBlock(features=["bold", "link", "italic"], required=False)),
                ], icon="image")),
                ("code", blocks.StructBlock([
                    ("language", blocks.CharBlock()),
                    ("code", blocks.TextBlock()),
                ], icon="code")),
            ])),
        ], icon="doc-full")),
    ], use_json_field=True)
    tags = ParentalManyToManyField("articles.ArticleTag", related_name="articles")

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("image"),
        FieldPanel("intro"),
        FieldPanel("body", ),
        FieldPanel("tags"),
    ]

    parent_page_type = ["articles.WritingPage"]

    preview_modes = []

    also_revalidate = ["/writing"]

    def __str__(self):
        return self.title


    def get_url(self, *args, **kwargs):
        return f"{settings.FRONTEND_URL}/writing/{self.slug}"
    

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
            elif block.block_type == "section":
                blocks.append({
                    "type": block.block_type,
                    "value": {
                        "title": block.value["title"],
                        "subtitle": block.value["subtitle"],
                        "body": [{
                            "type": subblock.block_type,
                            "value": subblock.render()
                        } for subblock in block.value["body"]]
                    }
                })
        return JsonResponse({
            "title": self.title,
            "image": self.image.file.url if self.image else None,
            "date": self.date,
            "body": blocks,
            "tags": [{"name": tag.name, "color": tag.color} for tag in self.tags.all()],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



@register_snippet
class ArticleTag(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name