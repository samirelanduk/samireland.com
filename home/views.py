from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from home.models import EditableText, Publication
from blog.models import BlogPost

# Create your views here.
def home_page(request):
    text = EditableText.objects.filter(name="home").first()
    text = text if text else ""
    post = BlogPost.objects.filter(visible=True).order_by("date").last()
    return render(request, "home.html", {"text": text, "post": post})


def about_page(request):
    text = EditableText.objects.filter(name="about").first()
    text = text if text else ""
    return render(request, "about.html", {"text": text})


def research_page(request):
    text = EditableText.objects.filter(name="research").first()
    text = text if text else ""
    return render(request, "research.html", {"text": text})


@login_required(login_url="/", redirect_field_name=None)
def new_research_page(request):
    if request.method == "POST":
        Publication.objects.create(
         pk=request.POST["id"], title=request.POST["title"],
         date=request.POST["date"], url=request.POST["url"],
         doi=request.POST["doi"], authors=request.POST["authors"],
         abstract=request.POST["abstract"], body=request.POST["body"]
        )
        return redirect("/research/{}/".format(request.POST["id"]))
    return render(request, "new-research.html")


def publication_page(request, pk):
    pub = Publication.objects.filter(pk=pk).first()
    if not pub:
        raise Http404
    return render(request, "publication.html", {"publication": pub})


def projects_page(request):
    projects_text = EditableText.objects.filter(name="projects").first()
    projects_text = projects_text if projects_text else ""
    return render(request, "projects.html", {"projects_text": projects_text})


def login_page(request):
    if request.method == "POST":
        user = authenticate(
         username=request.POST["username"],
         password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/youshallnotpass/")
    return render(request, "login.html")


def fence_page(request):
    return render(request, "fence.html")


def logout_page(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/", redirect_field_name=None)
def edit_page(request, name):
    ALLOWED_NAMES = {
     "home": "/",
     "about": "/about/",
     "research": "/research/",
     "projects": "/projects/"
    }
    if name not in ALLOWED_NAMES:
        raise Http404("Not a valid name")
    if request.method == "POST":
        if not EditableText.objects.filter(name=name):
            EditableText.objects.create(name=name, content=request.POST["content"])
        else:
            text = EditableText.objects.filter(name=name).first()
            text.content = request.POST["content"]
            text.save()
        return redirect(ALLOWED_NAMES[name])
    text = EditableText.objects.filter(name=name).first()
    text = text if text else ""
    return render(request, "edit.html", {"text": text})
