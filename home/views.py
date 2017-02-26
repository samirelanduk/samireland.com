from django.shortcuts import render, redirect

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def login_page(request):
    if request.method == "POST":
        return redirect("/")
    return render(request, "login.html")
