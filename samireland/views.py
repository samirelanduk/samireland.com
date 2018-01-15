"""Views for samireland.com"""

import os
import django.shortcuts as shortcuts
from django.http import Http404
from django.db import IntegrityError
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PublicationForm, ProjectForm

def home(request):
    text = grab_editable_text("home")
    return shortcuts.render(request, "home.html", {"text": text})


def research(request):
    text = grab_editable_text("research")
    return shortcuts.render(request, "research.html", {
     "text": text, "publications": Publication.objects.all().order_by("-date")
    })


@login_required(login_url="/", redirect_field_name=None)
def new_pub(request):
    if request.method == "POST":
        form = PublicationForm(request.POST)
        if form.is_valid():
            form.save()
            return shortcuts.redirect("/research/{}/".format(request.POST["id"]))
        else:
            return shortcuts.render(request, "new-pub.html", {"form": form})
    form = PublicationForm()
    return shortcuts.render(request, "new-pub.html", {"form": form})


def publication(request, id):
    try:
        publication = Publication.objects.get(id=id)
    except Publication.DoesNotExist:
        raise Http404
    return shortcuts.render(request, "publication.html", {"publication": publication})


@login_required(login_url="/", redirect_field_name=None)
def edit_pub(request, id):
    try:
        publication = Publication.objects.get(id=id)
    except Publication.DoesNotExist:
        raise Http404
    if request.method == "POST":
        if "delete" in request.POST:
            publication.delete()
            return shortcuts.redirect("/research/")
        request.POST = request.POST.copy()
        request.POST["id"] = id
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
        return shortcuts.redirect("/research/{}/".format(id))
    form = PublicationForm(instance=publication)
    return shortcuts.render(request, "edit-pub.html", {"form": form})


def projects(request):
    text = grab_editable_text("projects")
    return shortcuts.render(request, "projects.html", {
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
        return shortcuts.redirect("/projects/")
    form = ProjectForm()
    return shortcuts.render(request, "new-project.html", {"form": form})


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
        return shortcuts.redirect("/projects/")
    form = ProjectForm(instance=project)
    return shortcuts.render(request, "edit-project.html", {"form": form})


def writing(request):
    return shortcuts.render(request, "writing.html")


def about(request):
    text = grab_editable_text("about")
    return shortcuts.render(request, "about.html", {"text": text})


@login_required(login_url="/", redirect_field_name=None)
def media(request):
    if request.method == "POST":
        if "delete" in request.POST:
            media = MediaFile.objects.get(name=request.POST["name"])
            try:
                os.remove(media.mediafile.path)
            except FileNotFoundError: pass
            media.delete()
            return shortcuts.redirect("/media/")
        try:
            MediaFile.objects.create(
             name=request.POST["name"], mediafile=request.FILES["file"]
            )
        except IntegrityError:
            return shortcuts.render(request, "media.html", {
             "error": "There is already media with that name",
             "media": MediaFile.objects.all()
            })
        return shortcuts.redirect("/media/")
    return shortcuts.render(request, "media.html", {
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
            return shortcuts.redirect("/")
        return shortcuts.render(request, "login.html", {"error": "Nope!"})
    return shortcuts.render(request, "login.html")


def logout(request):
    auth.logout(request)
    return shortcuts.redirect("/")


def edit(request, name):
    if request.method == "POST":
        if request.user.is_authenticated:
            text = EditableText.objects.get(name=name)
            text.body = request.POST["body"]
            text.save()
            return shortcuts.redirect(request.POST["redirect"])
    raise Http404


def grab_editable_text(name):
    try:
        return EditableText.objects.get(name=name)
    except EditableText.DoesNotExist:
        return EditableText.objects.create(name=name, body="")
