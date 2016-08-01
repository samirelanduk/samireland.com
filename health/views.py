from django.shortcuts import render

# Create your views here.
def edit_page(request):
    return render(request, "edit_health.html")
