from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from media.models import MediaFile

# Create your views here.
@login_required(login_url="/", redirect_field_name=None)
def media_page(request):
    if request.method == "POST":
        media = MediaFile(
         mediatitle=request.POST["title"],
         mediafile=request.FILES["file"],
        )
        media.save()
        return redirect("/media/")
    return render(request, "media.html")
