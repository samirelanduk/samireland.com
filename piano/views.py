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

    today = datetime.now().date()
    today_minus_59 = datetime.now().date() - timedelta(days=59)
    relevant_sessions = PracticeSession.objects.filter(date__gte=today_minus_59)
    last_sixty = [[int(session.date.strftime("%s")) * 1000, session.minutes] for session in relevant_sessions]
    '''last_sixty_cumulative = [[sixty_days_ago, 0]]
    day = sixty_days_ago + timedelta(days=1)
    while day <= today:
        session = last_sixty_sessions.filter(date=day).first()
        if session:
            last_sixty_cumulative.append([day, session.cumulative_minutes])
        else:
            last_sixty_cumulative.append([day, last_sixty_cumulative[-1][1]])
        day += timedelta(days=1)
    last_sixty_cumulative = [[int(s[0].strftime("%s")), s[1]] for s in last_sixty_cumulative[1:]]'''
    return render(request, "piano.html", {
     "text": text,
     "practice_time": hours_text + minutes_text,
     "today": int(today.strftime("%s")) * 1000,
     "minus_59": int(today_minus_59.strftime("%s")) * 1000,
     "last_sixty": last_sixty
     # "last_sixty_cumulative": last_sixty_cumulative
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
