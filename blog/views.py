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
    if not request.user.is_authenticated():
        posts = posts.filter(visible=True)
    return render(request, "blog.html", {"posts": [p for p in posts]})


def one_post_page(request, year, month, day):
    date = datetime(int(year), int(month), int(day)).date()
    post = BlogPost.objects.filter(date=date).first()
    if not post or not post.visible:
        raise Http404
    previous = BlogPost.objects.filter(
     date__lt=date, visible=True
    ).order_by("date").last()
    next_ = BlogPost.objects.filter(
     date__gt=date, visible=True
    ).order_by("date").first()
    return render(request, "one-post.html", {
     "post": post, "previous": previous, "next": next_
    })


def year_page(request, year):
    year = int(year)
    all_posts = BlogPost.objects.filter(visible=True).order_by("date")
    posts = [post for post in all_posts if post.date.year == year]
    previous_years = [p for p in all_posts if p.date.year < year]
    next_years = [p for p in all_posts if p.date.year > year]
    prev = previous_years[-1].date.year if previous_years else None
    next_ = next_years[0].date.year if next_years else None
    if not posts: raise Http404
    return render(request, "year-posts.html", {
     "year": year, "posts": posts[::-1], "previous": prev, "next": next_
    })


def edit_post_page(request, year, month, day):
    date = datetime(int(year), int(month), int(day)).date()
    post = BlogPost.objects.filter(date=date).first()
    if not post:
        raise Http404
    if request.method == "POST":
        try:
            date = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()
        except:
            return render(request, "edit-blog.html", {
             "post": post, "error": "You cannot submit a post with no date"
            })
        if date != post.date and BlogPost.objects.filter(date=date):
            return render(request, "edit-blog.html", {
             "post": post, "error": "There is already a post with that date"
            })
        if not request.POST["title"]:
            return render(request, "edit-blog.html", {
             "post": post, "error": "You cannot submit a post with no title"
            })
        if not request.POST["body"]:
            return render(request, "edit-blog.html", {
             "post": post, "error": "You cannot submit a post with no body"
            })
        post.date = datetime.strptime(request.POST["date"], "%Y-%m-%d")
        post.title = request.POST["title"]
        post.body = request.POST["body"]
        post.visible = "visible" in request.POST
        post.save()
        if not post.visible: return redirect("/blog/")
        return redirect(post.date.strftime("/blog/%Y/%-m/%-d/"))
    return render(request, "edit-blog.html", {
     "post": post
    })


def delete_post_page(request, year, month, day):
    date = datetime(int(year), int(month), int(day)).date()
    post = BlogPost.objects.filter(date=date).first()
    if not post:
        raise Http404
    if request.method == "POST":
        post.delete()
        return redirect("/blog/")
    return render(request, "delete-blog.html", {
     "post": post
    })
