from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404
from blog.models import BlogPost

# Create your views here.
def new_blog_page(request):
    today = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        try:
            date = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()
        except:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no date"
            })
        if BlogPost.objects.filter(date=date):
            return render(request, "new-blog.html", {
             "today": today, "error": "There is already a post with that date"
            })
        if not request.POST["title"]:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no title"
            })
        if not request.POST["body"]:
            return render(request, "new-blog.html", {
             "today": today, "error": "You cannot submit a post with no body"
            })
        post = BlogPost.objects.create(
         date=request.POST["date"],
         title=request.POST["title"],
         body=request.POST["body"],
         visible="visible" in request.POST
        )
        post.save()
        return redirect("/blog/")
    return render(request, "new-blog.html", {"today": today})


def blog_page(request):
    posts = BlogPost.objects.all().order_by("date").reverse()
    if request.user.is_authenticated:
        posts = posts.filter(visible=True)
    return render(request, "blog.html", {"posts": [p for p in posts]})


def one_post_page(request, year, month, day):
    date = datetime(int(year), int(month), int(day)).date()
    post = BlogPost.objects.filter(date=date)
    if not post.exists():
        raise Http404
    return render(request, "one-post.html", {"post": post.first()})
