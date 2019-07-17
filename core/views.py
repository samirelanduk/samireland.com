from django.shortcuts import redirect, render
from .models import Project

def home(request, message=False):
    four_projects = Project.objects.all()[:4]
    return render(request, "home.html", {"projects": four_projects})