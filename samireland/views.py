"""Views for samireland.com"""

import django.shortcuts as shortcuts
from django.http import Http404
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from .models import EditableText, Publication
from .forms import PublicationForm

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
