from django.shortcuts import redirect, render, get_object_or_404
from .models import Project, Publication, Article, Period

def home(request):
    four_projects = Project.objects.all()[:4]
    articles = Article.objects.all()[:2]
    publication = Publication.objects.filter(starred=True).first()
    return render(request, "home.html", {
     "projects": four_projects, "articles": articles, "publication": publication
    })


def about(request):
    periods = Period.objects.all()
    return render(request, "about.html", {"periods": periods})


def projects(request):
    tech = Project.all_tech()
    projects = Project.objects.all()
    return render(request, "projects.html", {"tech": tech, "projects": projects})


def writing(request):
    articles = Article.objects.all()
    return render(request, "writing.html", {"articles": articles})


def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "article.html", {"article": article})


def research(request):
    publications = Publication.objects.all()
    return render(request, "research.html", {"publications": publications})


def publication(request, id):
    publication = get_object_or_404(Publication, id=id)
    return render(request, "publication.html", {"publication": publication})


def handler404(request, exception):
    return render(request, "404.html")