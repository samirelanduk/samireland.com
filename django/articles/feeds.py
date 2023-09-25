
from django.contrib.syndication.views import Feed
from articles.models import ArticlePage

class ArticlesFeed(Feed):
    title = "Sam Ireland Writing"
    link = "/writing"
    description = "Latest posts and articles by Sam Ireland."


    def items(self):
        return ArticlePage.objects.all().order_by("-date")


    def item_title(self, item):
        return item.title


    def item_description(self, item):
        return item.intro


    def item_link(self, item):
        return f"/writing/{item.slug}"