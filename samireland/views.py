"""Views for samireland.com"""

import os
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import *

def home(request):
    text = grab_editable_text("home")
    blog = BlogPost.objects.order_by("date").last()
    article = Article.objects.order_by("date").last()
    pub = Publication.objects.order_by("date").last()
    return render(request, "home.html", {
     "text": text, "post": blog, "article": article, "publication": pub
    })


def research(request):
    text = grab_editable_text("research")
    return render(request, "research.html", {
     "text": text, "publications": Publication.objects.all().order_by("-date")
    })


def publication(request, id):
    publication = get_object_or_404(Publication, id=id)
    return render(request, "publication.html", {"publication": publication})


def projects(request):
    text = grab_editable_text("projects")
    return render(request, "projects.html", {
     "text": text,
     "web_projects": Project.objects.filter(category="web").order_by("name"),
     "python_projects": Project.objects.filter(category="python").order_by("name"),
     "other_projects": Project.objects.filter(category="other").order_by("name")
    })


def writing(request):
    text = grab_editable_text("writing")
    return render(request, "writing.html", {
     "text": text, "articles": Article.objects.all().order_by("-date")
    })


def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "article.html", {"article": article})


def blog(request):
    return render(
     request, "blog.html", {"posts": BlogPost.objects.all().order_by("-date")}
    )


def blog_post(request, year, month, day):
    post = get_object_or_404(BlogPost, date="{}-{}-{}".format(year, month, day))
    return render(request, "blog-post.html", {"post": post})


def about(request):
    text = grab_editable_text("about")
    return render(request, "about.html", {"text": text})


def media(request):
    if request.method == "POST":
        if "delete" in request.POST:
            media = MediaFile.objects.get(name=request.POST["name"])
            try:
                os.remove(media.mediafile.path)
            except FileNotFoundError: pass
            media.delete()
            return redirect("/media/")
        try:
            MediaFile.objects.create(
             name=request.POST["name"], mediafile=request.FILES["file"]
            )
        except IntegrityError:
            return render(request, "media.html", {
             "error": "There is already media with that name",
             "media": MediaFile.objects.all()
            })
        return redirect("/media/")
    return render(request, "media.html", {
     "media": MediaFile.objects.all()
    })


def edit(request, name):
    if request.method == "POST":
        if request.user.is_authenticated:
            text = EditableText.objects.get(name=name)
            text.body = request.POST["body"]
            text.save()
            return redirect(request.POST["redirect"])
    raise Http404


def grab_editable_text(name):
    try:
        return EditableText.objects.get(name=name)
    except EditableText.DoesNotExist:
        return EditableText.objects.create(name=name, body="")
