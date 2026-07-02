from django.db import models
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.fields import RichTextField
from django.http import JsonResponse
from django.conf import settings
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet

@register_snippet
class BookCategory(models.Model):

    name = models.CharField(max_length=100)
    number = models.IntegerField()

    class Meta:
        ordering = ["number", "name"]

    def __str__(self):
        return self.name


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
            "queues": [{
                "title": queue.title,
                "description": queue.description,
                "slug": queue.slug,
                "books": [book.to_json() for book in BookPage.objects.child_of(queue).live().order_by("started")],
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

    subpage_types = ["reading.BookPage"]

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
            "books": [book.to_json() for book in BookPage.objects.child_of(self).live().order_by("started")],
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })



class BookPage(Page):

    subtitle = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    rating = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10")], null=True, blank=True)
    started = models.DateField()
    finished = models.DateField(null=True, blank=True)
    notes = RichTextField(max_length=10000, features=["bold", "link", "italic", "h2", "h3", "ol", "ul", "code", "strikethrough", "blockquote"], null=True, blank=True)
    category = models.ForeignKey(BookCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("author"),
        FieldPanel("year"),
        FieldPanel("image"),
        FieldPanel("rating"),
        FieldPanel("category"),
        FieldPanel("started"),
        FieldPanel("finished"),
        FieldPanel("notes"),
    ]

    parent_page_type = ["reading.QueuePage"]

    preview_modes = []

    @property
    def also_revalidate(self):
        parent = self.get_parent()
        paths = ["/reading", f"/reading/{parent.slug}", f"/reading/{parent.slug}/{self.slug}"]
        # Neighbours link back to this book, so their pages go stale too
        for neighbour in (self.previous_book(), self.next_book()):
            if neighbour:
                paths.append(f"/reading/{parent.slug}/{neighbour.slug}")
        return paths

    def __str__(self):
        return self.title

    def get_url(self, *args, **kwargs):
        parent = self.get_parent()
        grandparent = parent.get_parent()
        return f"{settings.FRONTEND_URL}/{grandparent.slug}/{parent.slug}/{self.slug}"

    def to_json(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "year": self.year,
            "slug": self.slug,
            "image": self.image.file.url if self.image else None,
            "rating": self.rating,
            "started": self.started,
            "finished": self.finished,
            "notes": str(RichText(self.notes)) if self.notes else None,
            "category": {
                "name": self.category.name,
                "number": self.category.number,
            } if self.category else None,
        }

    def serve(self, request, *args, **kwargs):
        return JsonResponse({
            **self.to_json(),
            "meta": {
                "title": self.seo_title or self.title,
                "description": self.search_description
            }
        })