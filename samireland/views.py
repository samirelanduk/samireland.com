"""Views for samireland.com"""

import os
from django.shortcuts import render, redirect
from django.http import Http404
from django.db import IntegrityError
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PublicationForm, ProjectForm, ArticleForm, BlogPostForm

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


@login_required(login_url="/", redirect_field_name=None)
def new_pub(request):
    if request.method == "POST":
        form = PublicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/research/{}/".format(request.POST["id"]))
        else:
            return render(request, "new-pub.html", {"form": form})
    form = PublicationForm()
    return render(request, "new-pub.html", {"form": form})


def publication(request, id):
    try:
        publication = Publication.objects.get(id=id)
    except Publication.DoesNotExist:
        raise Http404
    return render(request, "publication.html", {"publication": publication})


@login_required(login_url="/", redirect_field_name=None)
def edit_pub(request, id):
    try:
        publication = Publication.objects.get(id=id)
    except Publication.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "delete" in request.POST:
            publication.delete()
            return redirect("/research/")
        request.POST = request.POST.copy()
        request.POST["id"] = id
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
        return redirect("/research/{}/".format(id))
    form = PublicationForm(instance=publication)
    return render(request, "edit-pub.html", {"form": form})


def projects(request):
    text = grab_editable_text("projects")
    return render(request, "projects.html", {
     "text": text,
     "web_projects": Project.objects.filter(category="web").order_by("name"),
     "python_projects": Project.objects.filter(category="python").order_by("name"),
     "other_projects": Project.objects.filter(category="other").order_by("name")
    })


@login_required(login_url="/", redirect_field_name=None)
def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/projects/")
    form = ProjectForm()
    return render(request, "new-project.html", {"form": form})


@login_required(login_url="/", redirect_field_name=None)
def edit_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "delete" in request.POST:
            project.delete()
        else:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
        return redirect("/projects/")
    form = ProjectForm(instance=project)
    return render(request, "edit-project.html", {"form": form})


def writing(request):
    text = grab_editable_text("writing")
    return render(request, "writing.html", {
     "text": text, "articles": Article.objects.all().order_by("-date")
    })


@login_required(login_url="/", redirect_field_name=None)
def new_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/writing/{}/".format(request.POST["id"]))
        else:
            return render(request, "new-article.html", {"form": form})
    form = ArticleForm()
    return render(request, "new-article.html", {"form": form})


def article(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, "article.html", {"article": article})


@login_required(login_url="/", redirect_field_name=None)
def edit_article(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "delete" in request.POST:
            article.delete()
            return redirect("/writing/")
        request.POST = request.POST.copy()
        request.POST["id"] = id
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
        return redirect("/writing/{}/".format(id))
    form = ArticleForm(instance=article)
    return render(request, "edit-article.html", {"form": form})


def blog(request):
    return render(
     request, "blog.html", {"posts": BlogPost.objects.all().order_by("-date")}
    )


@login_required(login_url="/", redirect_field_name=None)
def new_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
             "/blog/{}/".format(request.POST["date"].replace("-", "/"))
            )
        else:
            return render(request, "new-blog.html", {"form": form})
    form = BlogPostForm()
    return render(request, "new-blog.html", {"form": form})


def blog_post(request, year, month, day):
    try:
        post = BlogPost.objects.get(date="{}-{}-{}".format(year, month, day))
    except BlogPost.DoesNotExist:
        raise Http404
    return render(request, "blog-post.html", {"post": post})


@login_required(login_url="/", redirect_field_name=None)
def edit_blog(request, year, month, day):
    date_string = "{}-{}-{}".format(year, month, day)
    try:
        post = BlogPost.objects.get(date=date_string)
    except BlogPost.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "delete" in request.POST:
            post.delete()
            return redirect("/blog/")
        request.POST = request.POST.copy()
        request.POST["date"] = date_string
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect("/blog/{}/{}/{}/".format(year, month, day))
    form = BlogPostForm(instance=post)
    return render(request, "edit-blog.html", {"form": form})


def about(request):
    text = grab_editable_text("about")
    return render(request, "about.html", {"text": text})


@login_required(login_url="/", redirect_field_name=None)
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


def login(request):
    if request.method == "POST":
        user = auth.authenticate(
         username=request.POST["username"],
         password=request.POST["password"]
        )
        if user:
            auth.login(request, user)
            return redirect("/")
        return render(request, "login.html", {"error": "Nope!"})
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


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
