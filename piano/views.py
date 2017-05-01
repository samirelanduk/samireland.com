from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from home.models import EditableText
from piano.models import PracticeSession

# Create your views here.
def piano_page(request):
    text = EditableText.objects.filter(name="piano-long").first()
    text = text if text else ""

    minus_60 = today() - timedelta(days=59)
    minus_365 = today() - timedelta(days=364)
    this_month = datetime(today().year, today().month, 1)
    first_session = PracticeSession.objects.order_by("date").first()
    pre_month = first_month = this_month
    if first_session:
        first_date = first_session.date
        first_month = datetime(first_date.year, first_date.month, 1)
        pre_month = datetime(
         first_date.year if first_date.month != 1 else first_date.year - 1,
         first_date.month - 1 if first_date.month != 1 else 12,
         1
        )

    return render(request, "piano.html", {
     "text": text,
     "practice_time": get_practice_time(),
     "today": int(today().strftime("%s") + "000"),
     "minus_60": int(minus_60.strftime("%s") + "000"),
     "minus_365": int(minus_365.strftime("%s") + "000"),
     "this_month": int(this_month.strftime("%s") + "000"),
     "first_month": int(first_month.strftime("%s") + "000"),
     "pre_month": int(pre_month.strftime("%s") + "000"),
     "last_sixty": get_last_sixty(),
     "last_sixty_cumulative": get_last_sixty_cumulative(),
     "last_year": get_last_year(),
     "last_year_cumulative": get_last_year_cumulative(),
     "all": get_all(),
     "all_cumulative": get_all_cumulative()
    })


@login_required(login_url="/", redirect_field_name=None)
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


@login_required(login_url="/", redirect_field_name=None)
def piano_delete_page(request, pk):
    if PracticeSession.objects.filter(pk=pk).count() == 0:
        return redirect("/piano/")
    session = PracticeSession.objects.get(pk=pk)
    if request.method == "POST":
        session.delete()
        return redirect("/piano/update/")
    return render(request, "piano-delete.html", {"session": session})


def today():
    return datetime.now().date()


def get_practice_time():
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
    return hours_text + minutes_text


def get_last_sixty():
    sessions = PracticeSession.objects.filter(
     date__gt=today() - timedelta(days=60)
    ).filter(date__lte=today()).order_by("date")
    return [[int(s.date.strftime("%s") + "000"), s.minutes] for s in sessions]


def get_last_sixty_cumulative():
    first_date = today() - timedelta(days=59)
    minutes_at_start = sum([
     session.minutes for session in PracticeSession.objects.filter(date__lt=first_date)
    ])
    dates = [first_date + timedelta(days=i) for i in range(60)]
    data = [[first_date, minutes_at_start]]
    for day in dates[1:]:
        session = PracticeSession.objects.filter(date=day)
        if session:
            data.append([day, session.first().cumulative_minutes])
        else:
            data.append([day, data[-1][1]])
    return [[int(day.strftime("%s") + "000"), minutes / 60] for day, minutes in data]


def get_last_year():
    sessions = PracticeSession.objects.filter(
     date__gt=today() - timedelta(days=365)
    ).filter(date__lte=today()).order_by("date")
    return [[int(s.date.strftime("%s") + "000"), s.minutes] for s in sessions]


def get_last_year_cumulative():
    first_date = today() - timedelta(days=364)
    minutes_at_start = sum([
     session.minutes for session in PracticeSession.objects.filter(date__lt=first_date)
    ])
    dates = [first_date + timedelta(days=i) for i in range(365)]
    data = [[first_date, minutes_at_start]]
    for day in dates[1:]:
        session = PracticeSession.objects.filter(date=day)
        if session:
            data.append([day, session.first().cumulative_minutes])
        else:
            data.append([day, data[-1][1]])
    return [[int(day.strftime("%s") + "000"), minutes / 60] for day, minutes in data]


def get_all():
    first_session = PracticeSession.objects.order_by("date").first()
    if first_session:
        all_sessions = list(PracticeSession.objects.all().order_by("date"))
        first_month =  datetime(first_session.date.year, first_session.date.month, 1).date()
        this_month = datetime(today().year, today().month, 1).date()
        data = [[first_month, sum([
         s.minutes for s in all_sessions if s.date.year == first_month.year and s.date.month == first_month.month
        ])]]
        while data[-1][0] != this_month:
            next_month = datetime(
             data[-1][0].year if data[-1][0].month != 12 else data[-1][0].year + 1,
             data[-1][0].month + 1 if data[-1][0].month != 12 else 1,
             1
            ).date()
            minutes = sum([s.minutes for s in all_sessions if s.date.year == next_month.year and s.date.month == next_month.month])
            data.append([next_month, minutes])
        return [[int(day.strftime("%s") + "000"), minutes] for day, minutes in data]
    else:
        return []


def get_all_cumulative():
    first_session = PracticeSession.objects.order_by("date").first()
    if first_session:
        all_data = get_all()
        first_month =  datetime(first_session.date.year, first_session.date.month, 1).date()
        pre_month = datetime(
         first_month.year if first_month.month != 1 else first_month.year - 1,
         first_month.month - 1 if first_month.month != 1 else 12,
         1
        ).date()
        data = [[int(pre_month.strftime("%s") + "000"), 0]] + all_data
        cum_data = []
        for index, day in enumerate(data):
            cum_data.append([day[0], sum([d[1] for d in data[:index + 1]]) / 60])
        return cum_data
    else:
        return []
