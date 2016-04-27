from django.shortcuts import render, redirect
from blog.models import BlogPost
import datetime

# Create your views here.

def home_page(request):
    latest_post = BlogPost.objects.all().filter(visible=True).order_by("date").last()
    return render(request, "home.html", {"blog_post": latest_post})


def about_page(request):
    return render(request, "about.html")


def blog_page(request):
    blog_posts = BlogPost.objects.all().filter(visible=True).order_by("date").reverse()
    return render(request, "blog.html", {"blog_posts": blog_posts})


def new_post_page(request):
    if request.method == "POST":
        post = BlogPost.objects.create(
         title=request.POST["title"],
         date=datetime.datetime.strptime(
          request.POST["date"], "%Y-%m-%d"
         ).date(),
         body=request.POST["body"],
         visible=request.POST.get("visible") is not None
        )
        post.full_clean()
        return redirect("/")
    return render(request, "new_post.html")


def edit_posts_page(request):
    blog_posts = BlogPost.objects.all().order_by("date").reverse()
    return render(request, "edit_posts.html", {"blog_posts": blog_posts})


def edit_post_page(request, post_id):
    blog_post = BlogPost.objects.get(pk=post_id)
    if request.method == "POST":
        blog_post.title = request.POST["title"]
        blog_post.date = datetime.datetime.strptime(
         request.POST["date"], "%Y-%m-%d"
        ).date()
        blog_post.body = request.POST["body"]
        blog_post.visible = request.POST.get("visible") is not None
        blog_post.save()
        blog_post.full_clean()
        return redirect("/blog/")

    return render(request, "edit_post.html", {
     "title": blog_post.title,
     "date": datetime.datetime.strftime(blog_post.date, "%Y-%m-%d"),
     "body": blog_post.body,
     "checked": "checked" if blog_post.visible else "",
     "id": blog_post.id
    })


def delete_post_page(request, post_id):
    if request.method == "POST":
        doomed_post = BlogPost.objects.get(pk=post_id)
        doomed_post.delete()
        return redirect("/blog/edit/")
    return render(request, "delete_post.html")
