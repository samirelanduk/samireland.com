from datetime import datetime
from django.shortcuts import render
from home.models import EditableText

# Create your views here.
def piano_page(request):
    text = EditableText.objects.filter(name="piano-long").first()
    text = text if text else ""
    return render(request, "piano.html", {"text": text})


def piano_update_page(request):
    return render(request, "piano-update.html", {
     "today": datetime.now().strftime("%Y-%m-%d")
    })
