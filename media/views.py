from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/", redirect_field_name=None)
def media_page(request):
    return render(request, "media.html")
