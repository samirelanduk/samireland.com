from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from media.forms import MediaForm
from media.models import MediaFile

# Create your views here.
@login_required(login_url="/", redirect_field_name=None)
def media_page(request):
    media = MediaFile.objects.all()
    return render(request, "media_page.html", {"media": media})


@login_required(login_url="/", redirect_field_name=None)
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


@login_required(login_url="/", redirect_field_name=None)
def delete_media_page(request, mediatitle):
    doomed_image = MediaFile.objects.get(mediatitle=mediatitle)
    if request.method == "POST":
        doomed_image.delete()
        return redirect("/media/")
    return render(request, "delete_media.html", {"media": doomed_image})
