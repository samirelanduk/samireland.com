from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from home.models import EditableText

# Create your views here.
def home_page(request):
    text = EditableText.objects.filter(name="home").first()
    text = text if text else ""
    return render(request, "home.html", {"text": text})


def about_page(request):
    text = EditableText.objects.filter(name="about").first()
    text = text if text else ""
    return render(request, "about.html", {"text": text})


def research_page(request):
    text = EditableText.objects.filter(name="research").first()
    text = text if text else ""
    return render(request, "research.html", {"text": text})


def project_page(request):
    return render(request, "project.html")


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
    ALLOWED_NAMES = {"home": "/", "about": "/about/", "research": "/research/"}
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
