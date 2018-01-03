"""Views for samireland.com"""

import django.shortcuts as shortcuts
from django.http import Http404
import django.contrib.auth as auth
from .models import EditableText

def home(request):
    try:
        text = EditableText.objects.get(name="home")
    except EditableText.DoesNotExist:
        text = EditableText.objects.create(name="home", body="")
    return shortcuts.render(request, "home.html", {"text": text})


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
