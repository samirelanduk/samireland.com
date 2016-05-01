from django.shortcuts import render, redirect
from media.forms import MediaForm

# Create your views here.
def media_page(request):
    return render(request, "media_page.html")


def upload_media_page(request):
    if request.method == "POST":
        return redirect("/media/")
    form = MediaForm()
    return render(request, "upload_media.html", {"form": form})


def delete_media_page(request, filename):
    return render(request, "delete_media.html")
