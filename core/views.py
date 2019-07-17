from django.shortcuts import redirect, render
from .models import Project, Publication

def home(request, message=False):
    four_projects = Project.objects.all()[:4]
    two_pubs = Publication.objects.all()[:2]
    return render(request, "home.html", {
     "projects": four_projects, "publications": two_pubs
    })