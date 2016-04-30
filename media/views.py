from django.shortcuts import render

# Create your views here.
def media_page(request):
    return render(request, "media_page.html")


def upload_media_page(request):
    return render(request, "upload_media.html")


def delete_media_page(request, filename):
    return render(request, "delete_media.html")
