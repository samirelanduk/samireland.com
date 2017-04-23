from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
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

    first_session = PracticeSession.objects.order_by("date").first()
    data = [[first_session.date, first_session.minutes, first_session.cumulative_minutes]]
    today = datetime.now().date()
    today_minus_59 = datetime.now().date() - timedelta(days=59)
    today_minus_364 = datetime.now().date() - timedelta(days=364)
    while data[-1][0] < today:
        day = data[-1][0] + timedelta(days=1)
        session = PracticeSession.objects.filter(date=day)
        if session:
            session = session.first()
            data.append([session.date, session.minutes, session.cumulative_minutes])
        else:
            data.append([day, 0, data[-1][-1]])

    data = [[int(d[0].strftime("%s")) * 1000, d[1], d[2]] for d in data]
    return render(request, "piano.html", {
     "text": text,
     "practice_time": hours_text + minutes_text,
     "today": int(today.strftime("%s")) * 1000,
     "minus_59": int(today_minus_59.strftime("%s")) * 1000,
     "minus_364": int(today_minus_364.strftime("%s")) * 1000,
     "last_sixty": [d[:2] for d in data[-60:] if d[1]],
     "last_sixty_cumulative": [[d[0], d[2]] for d in data[-60:]],
     "last_365": [d[:2] for d in data[-365:] if d[1]],
     "last_365_cumulative": [[d[0], d[2]] for d in data[-365:]],
    })


def piano_update_page(request):
    sessions = list(PracticeSession.objects.all().order_by("date").reverse())
    if request.method == "POST":
        error_text = None
        try:
            datetime.strptime(request.POST["date"], "%Y-%m-%d")
        except:
            error_text = "You cannot submit a session with no date"
        if not request.POST["minutes"]:
            error_text = "You cannot submit a session with no minutes"
        elif not request.POST["minutes"].isdigit():
            error_text = "Minutes have to be a number"
        if error_text:
            return render(request, "piano-update.html", {
             "today": datetime.now().strftime("%Y-%m-%d"),
             "sessions": sessions,
             "error_text": error_text
            })
        try:
            PracticeSession.objects.create(
             date=request.POST["date"],
             minutes=request.POST["minutes"]
            )
        except IntegrityError:
            return render(request, "piano-update.html", {
             "today": datetime.now().strftime("%Y-%m-%d"),
             "sessions": sessions,
             "error_text": "There is already a session for this date"
            })
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
