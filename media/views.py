from django.shortcuts import render, redirect
from media.forms import MediaForm
from media.models import Image

# Create your views here.
def media_page(request):
    images = Image.objects.all()
    return render(request, "media_page.html", {"images": images})


def upload_media_page(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/media/")
        else:
            return render(request, "upload_media.html", {"form": form})
    form = MediaForm()
    return render(request, "upload_media.html", {"form": form})


def delete_media_page(request, filename):
    return render(request, "delete_media.html")
