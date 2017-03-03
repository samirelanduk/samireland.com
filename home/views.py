from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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


def edit_page():
    pass
