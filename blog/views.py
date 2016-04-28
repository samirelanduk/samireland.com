from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
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
        try:
            post = BlogPost()
            post.title = request.POST["title"].strip()
            try:
                post.date = datetime.datetime.strptime(
                 request.POST["date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                post.body = "."
                post.visible = True
                post.date = datetime.datetime(1900, 1, 1)
                post.save()
                raise ValidationError("Invalid Date format")
            post.body = request.POST["body"].strip()
            post.visible = request.POST.get("visible") is not None
            post.save()
            post.full_clean()
        except ValidationError:
            post.delete()
            invalid_field = ""
            if not request.POST["title"].strip():
                invalid_field = "title"
            elif not request.POST["date"].strip():
                invalid_field = "date"
            else:
                invalid_field = "body"
            error_message = "You cannot submit a blog post with no %s" % invalid_field
            return render(request, "new_post.html", {"error": error_message})
        return redirect("/")
    return render(request, "new_post.html")


def edit_posts_page(request):
    blog_posts = BlogPost.objects.all().order_by("date").reverse()
    return render(request, "edit_posts.html", {"blog_posts": blog_posts})


def edit_post_page(request, post_id):
    blog_post = BlogPost.objects.get(pk=post_id)
    if request.method == "POST":
        try:
            blog_post.title = request.POST["title"].strip()
            try:
                blog_post.date = datetime.datetime.strptime(
                 request.POST["date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                blog_post.body = "."
                blog_post.visible = True
                blog_post.date = datetime.datetime(1900, 1, 1)
                blog_post.save()
                raise ValidationError("Invalid Date format")
            blog_post.body = request.POST["body"].strip()
            blog_post.visible = request.POST.get("visible") is not None
            blog_post.full_clean()
            blog_post.save()
        except ValidationError:
            invalid_field = ""
            if not request.POST["title"].strip():
                invalid_field = "title"
            elif not request.POST["date"].strip():
                invalid_field = "date"
            else:
                invalid_field = "body"
            error_message = "You cannot submit a blog post with no %s" % invalid_field
            blog_post = BlogPost.objects.get(pk=post_id)
            return render(request, "edit_post.html", {
             "title": blog_post.title,
             "date": datetime.datetime.strftime(blog_post.date, "%Y-%m-%d"),
             "body": blog_post.body,
             "checked": "checked" if blog_post.visible else "",
             "id": blog_post.id,
             "error": error_message
            })
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
