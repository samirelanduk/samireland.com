from testarsenal import DjangoTest
import samireland.views as views

class UrlTests(DjangoTest):

    def test_home_url(self):
        self.check_url_returns_view("/", views.home)


    def test_research_url(self):
        self.check_url_returns_view("/research/", views.research)


    def test_publication_url(self):
        self.check_url_returns_view("/research/ab-cd/", views.publication)


    def test_projects_url(self):
        self.check_url_returns_view("/projects/", views.projects)


    def test_writing_url(self):
        self.check_url_returns_view("/writing/", views.writing)


    def test_article_url(self):
        self.check_url_returns_view("/writing/ab-cd/", views.article)


    def test_blog_url(self):
        self.check_url_returns_view("/blog/", views.blog)


    def test_blog_post_url(self):
        self.check_url_returns_view("/blog/1111/22/33/", views.blog_post)


    def test_about_url(self):
        self.check_url_returns_view("/about/", views.about)


    def test_media_url(self):
        self.check_url_returns_view("/media/", views.media)
