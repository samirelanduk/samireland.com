from unittest.mock import patch, Mock
from testarsenal import DjangoTest
from django.http import Http404, QueryDict
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from samireland.models import EditableText
from samireland.views import *

class ViewTest(DjangoTest):

    def setUp(self):
        self.patcher1 = patch("samireland.views.grab_editable_text")
        self.mock_grab = self.patcher1.start()
        self.mock_grab.return_value = "EDTEXT"


    def tearDown(self):
        self.patcher1.stop()



class HomeViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.BlogPost.objects.order_by")
        self.patcher3 = patch("samireland.views.Article.objects.order_by")
        self.patcher4 = patch("samireland.views.Publication.objects.order_by")
        self.mock_blog = self.patcher2.start()
        self.mock_article = self.patcher3.start()
        self.mock_pub = self.patcher4.start()


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        ViewTest.tearDown(self)


    def test_home_view_uses_home_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(home, request, "home.html")


    def test_home_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(home, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("home")


    def test_home_view_can_send_latest_items(self):
        blogs, articles, pubs = Mock(), Mock(), Mock()
        blogs.last.return_value = "B"
        articles.last.return_value = "A"
        pubs.last.return_value = "P"
        self.mock_blog.return_value = blogs
        self.mock_article.return_value = articles
        self.mock_pub.return_value = pubs
        request = self.make_request("---")
        self.check_view_has_context(home, request, {"post": "B"})
        self.check_view_has_context(home, request, {"article": "A"})
        self.check_view_has_context(home, request, {"publication": "P"})
        self.mock_blog.assert_called_with("date")
        self.mock_article.assert_called_with("date")
        self.mock_pub.assert_called_with("date")



class ResearchViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Publication.objects.all")
        self.mock_all = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_research_view_uses_research_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(research, request, "research.html")


    def test_research_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(research, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("research")


    def test_research_view_sends_publications(self):
        request = self.make_request("---")
        all_pubs = Mock()
        self.mock_all.return_value = all_pubs
        ordered_pubs = Mock()
        all_pubs.order_by.return_value = ordered_pubs
        self.check_view_has_context(
         research, request, {"publications": ordered_pubs}
        )
        all_pubs.order_by.assert_called_with("-date")



class PublicationViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.get_object_or_404")
        self.mock_get = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_pub_view_uses_pub_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(
         publication, request, "publication.html", "abc"
        )


    def test_pub_view_can_get_publication(self):
        self.mock_get.return_value = "PUB"
        request = self.make_request("---")
        self.check_view_has_context(
         publication, request, {"publication": "PUB"}, "abc"
        )
        self.mock_get.assert_called_with(Publication, id="abc")



class ProjectsViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Project.objects.filter")
        self.mock_filter = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_projects_view_uses_projects_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(projects, request, "projects.html")


    def test_projects_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(projects, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("projects")


    def test_projects_view_sends_web_projects(self):
        request = self.make_request("---")
        web_projects = Mock()
        self.mock_filter.return_value = web_projects
        ordered_projects = Mock()
        web_projects.order_by.return_value = ordered_projects
        self.check_view_has_context(
         projects, request, {"web_projects": ordered_projects}
        )
        self.mock_filter.assert_any_call(category="web")
        web_projects.order_by.assert_called_with("name")


    def test_projects_view_sends_python_projects(self):
        request = self.make_request("---")
        python_projects = Mock()
        self.mock_filter.return_value = python_projects
        ordered_projects = Mock()
        python_projects.order_by.return_value = ordered_projects
        self.check_view_has_context(
         projects, request, {"python_projects": ordered_projects}
        )
        self.mock_filter.assert_any_call(category="python")
        python_projects.order_by.assert_called_with("name")


    def test_projects_view_sends_other_projects(self):
        request = self.make_request("---")
        other_projects = Mock()
        self.mock_filter.return_value = other_projects
        ordered_projects = Mock()
        other_projects.order_by.return_value = ordered_projects
        self.check_view_has_context(
         projects, request, {"other_projects": ordered_projects}
        )
        self.mock_filter.assert_any_call(category="other")
        other_projects.order_by.assert_called_with("name")



class WritingViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Article.objects.all")
        self.mock_all = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_writing_view_uses_writing_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(writing, request, "writing.html")


    def test_writing_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(writing, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("writing")


    def test_writing_view_sends_articles(self):
        request = self.make_request("---")
        all_articles = Mock()
        self.mock_all.return_value = all_articles
        ordered_articles = Mock()
        all_articles.order_by.return_value = ordered_articles
        self.check_view_has_context(
         writing, request, {"articles": ordered_articles}
        )
        all_articles.order_by.assert_called_with("-date")



class ArticleViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.get_object_or_404")
        self.mock_get = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_article_view_uses_article_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(
         article, request, "article.html", "abc"
        )


    def test_article_view_can_get_article(self):
        self.mock_get.return_value = "ARTICLE"
        request = self.make_request("---")
        self.check_view_has_context(
         article, request, {"article": "ARTICLE"}, "abc"
        )
        self.mock_get.assert_called_with(Article, id="abc")



class BlogViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.BlogPost.objects.all")
        self.mock_all = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_blog_view_uses_blog_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(blog, request, "blog.html")


    def test_blog_view_sends_blog_posts(self):
        request = self.make_request("---")
        all_posts = Mock()
        self.mock_all.return_value = all_posts
        ordered_posts = Mock()
        all_posts.order_by.return_value = ordered_posts
        self.check_view_has_context(
         blog, request, {"posts": ordered_posts}
        )
        all_posts.order_by.assert_called_with("-date")



class BlogPostViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.get_object_or_404")
        self.mock_get = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_blog_post_view_uses_blog_post_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(
         blog_post, request, "blog-post.html", "1000", "20", "30"
        )


    def test_blog_post_view_can_get_blog_post(self):
        self.mock_get.return_value = "POST"
        request = self.make_request("---")
        self.check_view_has_context(
         blog_post, request, {"post": "POST"}, "1000", "20", "30"
        )
        self.mock_get.assert_called_with(BlogPost, date="1000-20-30")



class AboutViewTests(ViewTest):

    def test_about_view_uses_about_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(about, request, "about.html")


    def test_about_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(about, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("about")



class MediaViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.MediaFile.objects.all")
        self.patcher3 = patch("samireland.views.MediaFile.objects.get")
        self.mock_all = self.patcher2.start()
        self.mock_get = self.patcher3.start()


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        ViewTest.tearDown(self)


    def test_media_view_uses_media_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(media, request, "media.html")


    def test_media_view_can_send_media(self):
        self.mock_all.return_value = [1, 2, 3]
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(media, request, {"media": [1, 2, 3]})
        self.mock_all.assert_called_with()



class EditableTextGrabberTests(DjangoTest):

    def setUp(self):
        self.patcher1 = patch("samireland.views.EditableText.objects.create")
        self.patcher2 = patch("samireland.views.EditableText.objects.get")
        self.mock_create = self.patcher1.start()
        self.mock_get = self.patcher2.start()
        self.mock_create.return_value = "EDTEXT"
        self.mock_get.side_effect = EditableText.DoesNotExist


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()


    def test_grabber_can_create_and_return_text(self):
        text = grab_editable_text("xxx")
        self.assertEqual(text, "EDTEXT")
        self.mock_create.assert_called_with(name="xxx", body="")


    def test_home_view_can_obtain_and_send_text(self):
        self.mock_get.side_effect = ["EDTEXT"]
        text = grab_editable_text("xxx")
        self.assertEqual(text, "EDTEXT")
        self.assertFalse(self.mock_create.called)
        self.mock_get.assert_called_with(name="xxx")
