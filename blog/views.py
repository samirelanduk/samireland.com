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
        BlogPost.objects.create(
         title=request.POST["title"],
         date=datetime.datetime.strptime(
          request.POST["date"], "%Y-%m-%d"
         ).date(),
         body=request.POST["body"],
         visible=request.POST.get("visible") is not None
        )
        return redirect("/")
    return render(request, "new_post.html")


def edit_posts_page(request):
    blog_posts = BlogPost.objects.all().order_by("date").reverse()
    return render(request, "edit_posts.html", {"blog_posts": blog_posts})


def edit_post_page(request, post_id):
    return render(request, "edit_post.html")
