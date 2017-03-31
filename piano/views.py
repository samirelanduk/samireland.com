from datetime import datetime
from django.shortcuts import render, redirect
from home.models import EditableText
from piano.models import PracticeSession

# Create your views here.
def piano_page(request):
    text = EditableText.objects.filter(name="piano-long").first()
    text = text if text else ""
    total_minutes = sum([
     session.minutes for session in PracticeSession.objects.all()
    ])
    hours = total_minutes // 60
    minutes = total_minutes % 60
    hours_text = "%i hour%s" % (hours, "s" if hours != 1 else "")
    if minutes and not hours: hours_text = ""
    minutes_text = "%s%i minutes" % (
     " and " if hours else "", minutes
    ) if minutes else ""
    return render(request, "piano.html", {
     "text": text,
     "practice_time": hours_text + minutes_text
    })


def piano_update_page(request):
    if request.method == "POST":
        PracticeSession.objects.create(
         date=request.POST["date"],
         minutes=request.POST["minutes"]
        )
        return redirect("/piano/update/")
    sessions = list(PracticeSession.objects.all().order_by("date").reverse())
    return render(request, "piano-update.html", {
     "today": datetime.now().strftime("%Y-%m-%d"),
     "sessions": sessions
    })
