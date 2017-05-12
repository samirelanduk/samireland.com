from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/", redirect_field_name=None)
def media_page(request):
    if request.method == "POST":
        return redirect("/media/")
    return render(request, "media.html")
