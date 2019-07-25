from django.shortcuts import redirect, render, get_object_or_404
from .models import Project, Publication, Article, Period

def home(request):
    four_projects = Project.objects.all()[:4]
    two_pubs = Publication.objects.all()[:2]
    article = Article.objects.first()
    return render(request, "home.html", {
     "projects": four_projects, "publications": two_pubs, "article": article
    })


def about(request):
     periods = Period.objects.all()
     return render(request, "about.html", {"periods": periods})


def projects(request):
     tech = Project.all_tech()
     projects = Project.objects.all()
     return render(request, "projects.html", {"tech": tech, "projects": projects})


def article(request, id):
     article = get_object_or_404(Article, id=id)
     return render(request, "article.html", {"article": article})