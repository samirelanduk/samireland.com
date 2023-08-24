from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
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
            } for article in ArticlePage.objects.all().order_by("-date")]
        })




class ArticlePage(Page):

    date = models.DateField("Article date")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    intro = models.TextField()
    body = StreamField([
        ("text", blocks.RichTextBlock(features=["bold", "link", "italic", "h2", "h3", "ol", "ul", "code", "strikethrough"])),
        ("image", ImageChooserBlock()),
        ("figure", blocks.StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", blocks.RichTextBlock(features=["bold", "link", "italic"])),
        ], icon="image")),
        ("code", blocks.StructBlock([
            ("language", blocks.CharBlock()),
            ("code", blocks.TextBlock()),
        ], icon="code")),
    ], use_json_field=True)
    tags = ClusterTaggableManager(through="articles.ArticleTag", blank=True)

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
        return JsonResponse({
            "title": self.title,
            "date": self.date,
            "body": [{
                "type": block.block_type,
                "value": block.render(),
            } for block in self.body]
        })


class ArticleTag(TaggedItemBase):
    
    content_object = ParentalKey(ArticlePage, on_delete=models.CASCADE, related_name="tagged_articles")