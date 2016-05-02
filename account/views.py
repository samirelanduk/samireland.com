from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_page(request):
    if request.method == "POST":
        user = authenticate(
         username=request.POST["username"],
         password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
        else:
            return redirect("/account/youshallnotpass/")
        return redirect("/")
    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/")

def barrier_page(request):
    return render(request, "barrier.html")
