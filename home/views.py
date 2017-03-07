from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from home.models import EditableText

# Create your views here.
def home_page(request):
    return render(request, "home.html")


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


def edit_page(request, name):
    ALLOWED_NAMES = ("home")
    if name not in ALLOWED_NAMES:
        raise Http404("Not a valid name")
    if request.method == "POST":
        if not EditableText.objects.filter(name=name):
            EditableText.objects.create(name=name, content=request.POST["content"])
        else:
            text = EditableText.objects.filter(name=name).first()
            text.content = request.POST["content"]
            text.save()
        return redirect("/")
    return render(request, "edit.html")
