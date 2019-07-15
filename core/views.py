from django.shortcuts import redirect, render

def home(request, message=False):
    return render(request, "home.html")