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
    sessions = list(PracticeSession.objects.all().order_by("date").reverse())
    if request.method == "POST":
        try:
            datetime.strptime(request.POST["date"], "%Y-%m-%d")
        except:
            return render(request, "piano-update.html", {
             "today": datetime.now().strftime("%Y-%m-%d"),
             "sessions": sessions,
             "error_text": "You cannot submit a session with no date"
            })
        PracticeSession.objects.create(
         date=request.POST["date"],
         minutes=request.POST["minutes"]
        )
        return redirect("/piano/update/")
    return render(request, "piano-update.html", {
     "today": datetime.now().strftime("%Y-%m-%d"),
     "sessions": sessions
    })


def piano_delete_page(request, pk):
    if PracticeSession.objects.filter(pk=pk).count() == 0:
        return redirect("/piano/")
    session = PracticeSession.objects.get(pk=pk)
    if request.method == "POST":
        session.delete()
        return redirect("/piano/update/")
    return render(request, "piano-delete.html", {"session": session})
