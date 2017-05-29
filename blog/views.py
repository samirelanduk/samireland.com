from datetime import datetime
from django.shortcuts import render, redirect

# Create your views here.
def new_blog_page(request):
    if request.method == "POST":
        return redirect("/blog/")
    today = datetime.now().strftime("%Y-%m-%d")
    return render(request, "new-blog.html", {"today": today})


def blog_page(request):
    return render(request, "blog.html")
