"""Views for samireland.com"""

import django.shortcuts as shortcuts
from django.http import Http404
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from .models import EditableText

def home(request):
    text = grab_editable_text("home")
    return shortcuts.render(request, "home.html", {"text": text})


def research(request):
    text = grab_editable_text("research")
    return shortcuts.render(request, "research.html", {"text": text})


@login_required(login_url="/", redirect_field_name=None)
def new_pub(request):
    return shortcuts.render(request, "new-pub.html")


def about(request):
    text = grab_editable_text("about")
    return shortcuts.render(request, "about.html", {"text": text})


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
