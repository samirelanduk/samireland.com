from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from blog.models import BlogPost
from blog.forms import BlogPostForm
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
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            return render(request, "new_post.html", {"form": form})
    form = BlogPostForm()
    return render(request, "new_post.html", {"form": form})


def edit_posts_page(request):
    blog_posts = BlogPost.objects.all().order_by("date").reverse()
    return render(request, "edit_posts.html", {"blog_posts": blog_posts})


def edit_post_page(request, post_id):
    blog_post = BlogPost.objects.get(pk=post_id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect("/blog/")
        else:
            return render(request, "edit_post.html", {"form": form, "id": post_id})
    else:
        form = BlogPostForm(instance=blog_post)
        return render(request, "edit_post.html", {"form": form, "id": post_id})


def delete_post_page(request, post_id):
    doomed_post = BlogPost.objects.get(pk=post_id)
    if request.method == "POST":
        doomed_post.delete()
        return redirect("/blog/edit/")
    return render(request, "delete_post.html", {"title": doomed_post.title})
