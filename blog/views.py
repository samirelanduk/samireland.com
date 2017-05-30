from datetime import datetime
from django.shortcuts import render, redirect
from blog.models import BlogPost

# Create your views here.
def new_blog_page(request):
    if request.method == "POST":
        post = BlogPost.objects.create(
         date=request.POST["date"],
         title=request.POST["title"],
         body=request.POST["body"],
         visible="visible" in request.POST
        )
        post.save()
        return redirect("/blog/")
    today = datetime.now().strftime("%Y-%m-%d")
    return render(request, "new-blog.html", {"today": today})


def blog_page(request):
    posts = [post for post in BlogPost.objects.all().order_by("date").reverse()]
    return render(request, "blog.html", {"posts": posts})
