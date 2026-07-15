import re

from django.http import JsonResponse
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page
from wagtail.rich_text import RichText

from about.models import AboutPage
from articles.models import ArticlePage, WritingPage
from projects.models import ProjectsPage
from reading.models import BookPage, QueuePage, ReadingPage


def frontend_slug(text):
    """Matches the slugify used for project anchors in next/src/utils.js."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def clean_text(html):
    return re.sub(r"\s+", " ", strip_tags(str(RichText(html)) if html else "")).strip()


def event_years(event):
    start = event.start[:4]
    end = event.end[:4] if event.end else ""
    if end == start: return start
    return f"{start}–{end}" if end else f"{start}–"


@cache_page(60 * 5)
def search_index(request):
    entries = []

    about_page = AboutPage.objects.live().first()
    projects_page = ProjectsPage.objects.live().first()
    writing_page = WritingPage.objects.live().first()
    reading_page = ReadingPage.objects.live().first()

    for page in (about_page, projects_page, writing_page, reading_page):
        if page is None:
            continue
        entries.append({
            "type": "page",
            "title": page.title,
            "url": f"/{page.slug}/",
            "image": None,
            "subtitle": page.search_description or clean_text(page.text),
            "meta": "",
            "keywords": "",
            "body": clean_text(page.text)[:500],
        })

    queues = QueuePage.objects.live() if reading_page else QueuePage.objects.none()

    for queue in queues:
        entries.append({
            "type": "page",
            "title": queue.title,
            "url": f"/{reading_page.slug}/{queue.slug}/",
            "image": None,
            "subtitle": queue.description or "",
            "meta": "",
            "keywords": "reading books queue",
            "body": "",
        })

    if about_page:
        events = [(event, None) for event in about_page.events.all()]
        events += [
            (subevent, event.name)
            for event in about_page.events.all()
            for subevent in event.subevents.all()
        ]
        for event, parent_name in events:
            description = clean_text(event.description)
            entries.append({
                "type": "event",
                "title": event.name,
                "url": f"/{about_page.slug}/",
                "image": event.image.file.url if event.image else None,
                "subtitle": description[:200],
                "meta": event_years(event),
                "keywords": parent_name or "",
                "body": description[:500],
            })

    if writing_page:
        for article in ArticlePage.objects.live().order_by("-date"):
            intro = re.sub(r"\s+", " ", article.intro or "").strip()
            entries.append({
                "type": "article",
                "title": article.title,
                "url": f"/{writing_page.slug}/{article.slug}/",
                "image": article.image.file.url if article.image else None,
                "subtitle": intro,
                "meta": article.date,
                "keywords": " ".join(tag.name for tag in article.tags.all()),
                "body": intro[:500],
            })

    for queue in queues:
        for book in BookPage.objects.child_of(queue).live().order_by("started"):
            entries.append({
                "type": "book",
                "title": book.title,
                "url": f"/{reading_page.slug}/{queue.slug}/{book.slug}/",
                "image": book.image.file.url if book.image else None,
                "subtitle": book.author,
                "meta": f"{book.rating}/10" if book.rating else ("" if book.finished else "Reading now"),
                "current": book.finished is None,
                "keywords": " ".join(filter(None, [
                    book.author,
                    book.category.name if book.category else None,
                    queue.title,
                    str(book.year),
                ])),
                "body": clean_text(book.notes)[:500],
            })

    if projects_page:
        for project in projects_page.projects.all():
            description = clean_text(project.description)
            entries.append({
                "type": "project",
                "title": project.name,
                "url": f"/{projects_page.slug}/#{frontend_slug(project.name)}",
                "image": project.image.file.url if project.image else None,
                "subtitle": description[:200],
                "meta": "",
                "keywords": " ".join(tag.name for tag in project.tags.all()),
                "body": description[:500],
            })

    return JsonResponse({"entries": entries})
