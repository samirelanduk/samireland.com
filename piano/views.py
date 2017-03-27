from django.shortcuts import render

# Create your views here.
def piano_page(request):
    return render(request, "piano.html")
