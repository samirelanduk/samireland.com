from blog.models import BlogPost

def years_processor(request):
    visible_posts = BlogPost.objects.filter(visible=True)
    years = [post.date.year for post in visible_posts]
    years = sorted(set(years), reverse=True)
    return {"blog_years": years}
