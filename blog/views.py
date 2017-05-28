from datetime import datetime
from django.shortcuts import render

# Create your views here.
def new_blog_page(request):
    today = datetime.now().strftime("%Y-%m-%d")
    return render(request, "new-blog.html", {"today": today})
