from django.shortcuts import render

# Create your views here.
def new_blog_page(request):
    return render(request, "new-blog.html")
