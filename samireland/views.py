"""Views for samireland.com"""

import django.shortcuts as shortcuts
import django.contrib.auth as auth

def home(request):
    return shortcuts.render(request, "home.html")


def login(request):
    if request.method == "POST":
        user = auth.authenticate(
         request,
         username=request.POST["username"],
         password=request.POST["password"]
        )
        if user:
            auth.login(request, user)
            return shortcuts.redirect("/")
    return shortcuts.render(request, "login.html")
