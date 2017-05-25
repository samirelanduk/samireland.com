from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from media.models import MediaFile

# Create your views here.
@login_required(login_url="/", redirect_field_name=None)
def media_page(request):
    if request.method == "POST":
        if not request.FILES.get("file"):
            return render(request, "media.html", {
             "media": MediaFile.objects.all(),
             "error_text": "You must supply a file."}
            )
        if not request.POST["title"]:
            return render(request, "media.html", {
             "media": MediaFile.objects.all(),
             "error_text": "You must supply a title."}
            )
        if MediaFile.objects.all().filter(mediatitle=request.POST["title"]):
            return render(request, "media.html", {
             "media": MediaFile.objects.all(),
             "error_text": "There is already a file with title."}
            )
        media = MediaFile(
         mediatitle=request.POST["title"],
         mediafile=request.FILES["file"],
        )
        media.save()
        return redirect("/media/")
    media = MediaFile.objects.all()
    return render(request, "media.html", {"media": media})


@login_required(login_url="/", redirect_field_name=None)
def media_delete_page(request, title):
    media = MediaFile.objects.filter(mediatitle=title)
    if media:
        if request.method == "POST":
            media.delete()
            return redirect("/media/")
        return render(request, "media-delete.html", {"media": media.first()})
    else:
        return redirect("/media/")
