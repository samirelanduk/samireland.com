from django.shortcuts import render

# Create your views here.
def piano_page(request):
    return render(request, "piano.html")


def practice_page(request):
    return render(request, "pianopractice.html")


def update_page(request):
    return render(request, "pianoupdate.html")
