import requests
import datetime
from django.shortcuts import render, redirect
from piano.models import PracticeSession
from piano.forms import PracticeSessionForm

# Create your views here.
def piano_page(request):
    yt_html = requests.get(
     "https://www.youtube.com/channel/UCILeIbhtlv4lmgAaZbPKr8A"
    ).text
    title_start = yt_html.find('<h3 class="yt-lockup-title ">')
    href_start = yt_html[title_start:].find("href=")
    href_end = yt_html[title_start + href_start:].find(">")
    yt_code = yt_html[
     title_start + href_start:title_start + href_start + href_end
    ].split("=")[-1].split('"')[0]
    return render(request, "piano.html", {"recent_code": yt_code})


def practice_page(request):
    return render(request, "pianopractice.html")


def update_page(request):
    today = datetime.datetime.now()
    form = PracticeSessionForm(initial={"date": today})
    if request.method == "POST":
        if "minutes" in request.POST:
            form = PracticeSessionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/piano/update/")
            else:
                return render(request, "pianoupdate.html", {"form": form})
        else:
            doomed_post = PracticeSession.objects.get(date=request.POST["date"])
            doomed_post.delete()
            return redirect("/piano/update/")

    sessions = PracticeSession.objects.all().order_by("date").reverse()
    return render(request, "pianoupdate.html", {"form": form, "sessions": sessions})
