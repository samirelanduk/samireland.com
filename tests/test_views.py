from unittest.mock import patch, Mock
from seleniumx import TestCaseX
from django.http import Http404, QueryDict
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from samireland.models import EditableText
from samireland.views import *

class ViewTest(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("samireland.views.grab_editable_text")
        self.mock_grab = self.patcher1.start()
        self.mock_grab.return_value = "EDTEXT"


    def tearDown(self):
        self.patcher1.stop()



class HomeViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(home, request, "home.html")


    def test_home_view_can_send_text(self):
        request = self.make_request("---")
        self.check_view_has_context(home, request, {"text": "EDTEXT"})
        self.mock_grab.assert_called_with("home")



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



class NewPublicationViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.PublicationForm")
        self.mock_form = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_new_pub_view_uses_new_pub_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(new_pub, request, "new-pub.html")


    def test_new_pub_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(new_pub, request, "/")


    def test_new_pub_sends_fresh_form(self):
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(new_pub, request, {"form": "FORM"})
        self.mock_form.assert_called_with()


    def test_new_pub_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"id": "xxx"}, loggedin=True
        )
        self.check_view_redirects(new_pub, request, "/research/xxx/")


    def test_new_pub_can_create_publication(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"id": "xxx", "b": "C"}, loggedin=True
        )
        new_pub(request)
        self.mock_form.assert_called_with(QueryDict("id=xxx&b=C"))
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_new_pub_validation(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = False
        request = self.make_request(
         "---", method="post", data={"id": "xxx", "b": "C"}, loggedin=True
        )
        self.check_view_uses_template(new_pub, request, "new-pub.html")
        self.check_view_has_context(new_pub, request, {"form": form})
        self.mock_form.assert_called_with(QueryDict("id=xxx&b=C"))
        form.is_valid.assert_called_with()



class PublicationViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Publication.objects.get")
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
        self.mock_get.assert_called_with(id="abc")


    def test_can_get_404_publication(self):
        self.mock_get.side_effect = Publication.DoesNotExist
        request = self.make_request("---")
        with self.assertRaises(Http404):
            publication(request, "abc")
        self.mock_get.assert_called_with(id="abc")



class EditPublicationViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Publication.objects.get")
        self.patcher3 = patch("samireland.views.PublicationForm")
        self.mock_get = self.patcher2.start()
        self.mock_form = self.patcher3.start()


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        ViewTest.tearDown(self)


    def test_edit_pub_view_uses_edit_pub_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(edit_pub, request, "edit-pub.html", "id")


    def test_edit_pub_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(edit_pub, request, "/", "id")


    def test_edit_pub_page_can_send_correct_form(self):
        self.mock_get.return_value = "PUB"
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(edit_pub, request, {"form": "FORM"}, "id")
        self.mock_get.assert_called_with(id="id")
        self.mock_form.assert_called_with(instance="PUB")


    def test_can_raise_404_publication(self):
        self.mock_get.side_effect = Publication.DoesNotExist
        request = self.make_request("---", loggedin=True)
        with self.assertRaises(Http404):
            edit_pub(request, "abc")
        self.mock_get.assert_called_with(id="abc")


    def test_edit_pub_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        self.check_view_redirects(edit_pub, request, "/research/xxx/", "xxx")


    def test_edit_pub_can_edit_publication(self):
        self.mock_get.return_value = "PUB"
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        edit_pub(request, "abc")
        self.mock_get.assert_called_with(id="abc")
        self.mock_form.assert_called_with(QueryDict("z=a&id=abc"), instance="PUB")
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_edit_pub_view_can_delete_publication(self):
        request = self.make_request(
         "---", method="post", data={"delete": "yes"}, loggedin=True
        )
        pub = Mock()
        self.mock_get.return_value = pub
        self.check_view_redirects(edit_pub, request, "/research/", "abc")
        pub.delete.assert_called_with()
        self.mock_get.assert_called_with(id="abc")



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



class NewProjectViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.ProjectForm")
        self.mock_form = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_new_project_view_uses_new_project_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(new_project, request, "new-project.html")


    def test_new_project_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(new_project, request, "/")


    def test_new_project_sends_fresh_form(self):
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(new_project, request, {"form": "FORM"})
        self.mock_form.assert_called_with()


    def test_new_project_redirects_on_post(self):
        request = self.make_request("---", method="post", loggedin=True)
        self.check_view_redirects(new_project, request, "/projects/")


    def test_new_project_can_create_project(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"id": "xxx", "b": "C"}, loggedin=True
        )
        new_project(request)
        self.mock_form.assert_called_with(QueryDict("id=xxx&b=C"))
        form.is_valid.assert_called_with()
        form.save.assert_called_with()



class EditProjectViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Project.objects.get")
        self.patcher3 = patch("samireland.views.ProjectForm")
        self.mock_get = self.patcher2.start()
        self.mock_form = self.patcher3.start()


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        ViewTest.tearDown(self)


    def test_edit_project_view_uses_edit_project_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(edit_project, request, "edit-project.html", "1")


    def test_edit_project_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(edit_project, request, "/", "id")


    def test_edit_project_page_can_send_correct_form(self):
        self.mock_get.return_value = "PUB"
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(edit_project, request, {"form": "FORM"}, "id")
        self.mock_get.assert_called_with(id="id")
        self.mock_form.assert_called_with(instance="PUB")


    def test_can_raise_404_project(self):
        self.mock_get.side_effect = Project.DoesNotExist
        request = self.make_request("---", loggedin=True)
        with self.assertRaises(Http404):
            edit_project(request, "abc")
        self.mock_get.assert_called_with(id="abc")


    def test_edit_project_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        self.check_view_redirects(edit_project, request, "/projects/", "xxx")


    def test_edit_project_can_edit_project(self):
        self.mock_get.return_value = "PUB"
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        edit_project(request, "23")
        self.mock_get.assert_called_with(id="23")
        self.mock_form.assert_called_with(QueryDict("z=a"), instance="PUB")
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_edit_project_redirects_on_deletion_post(self):
        request = self.make_request(
         "---", method="post", data={"delete": "yes"}, loggedin=True
        )
        self.check_view_redirects(edit_project, request, "/projects/", "xxx")


    def test_edit_project_view_can_delete_project(self):
        request = self.make_request(
         "---", method="post", data={"delete": "yes"}, loggedin=True
        )
        project = Mock()
        self.mock_get.return_value = project
        edit_project(request, "23")
        project.delete.assert_called_with()
        self.mock_get.assert_called_with(id="23")



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



class NewArticleViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.ArticleForm")
        self.mock_form = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_new_article_view_uses_new_article_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(new_article, request, "new-article.html")


    def test_new_article_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(new_article, request, "/")


    def test_new_article_sends_fresh_form(self):
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(new_article, request, {"form": "FORM"})
        self.mock_form.assert_called_with()


    def test_new_article_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"id": "xxx"}, loggedin=True
        )
        self.check_view_redirects(new_article, request, "/writing/xxx/")


    def test_new_article_can_create_article(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"id": "xxx", "b": "C"}, loggedin=True
        )
        new_article(request)
        self.mock_form.assert_called_with(QueryDict("id=xxx&b=C"))
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_new_article_validation(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = False
        request = self.make_request(
         "---", method="post", data={"id": "xxx", "b": "C"}, loggedin=True
        )
        self.check_view_uses_template(new_article, request, "new-article.html")
        self.check_view_has_context(new_article, request, {"form": form})
        self.mock_form.assert_called_with(QueryDict("id=xxx&b=C"))
        form.is_valid.assert_called_with()



class ArticleViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Article.objects.get")
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
        self.mock_get.assert_called_with(id="abc")


    def test_can_get_404_publication(self):
        self.mock_get.side_effect = Article.DoesNotExist
        request = self.make_request("---")
        with self.assertRaises(Http404):
            article(request, "abc")
        self.mock_get.assert_called_with(id="abc")



class EditArticleViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.Article.objects.get")
        self.patcher3 = patch("samireland.views.ArticleForm")
        self.mock_get = self.patcher2.start()
        self.mock_form = self.patcher3.start()


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        ViewTest.tearDown(self)


    def test_edit_article_view_uses_edit_article_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(edit_article, request, "edit-article.html", "id")


    def test_edit_article_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(edit_article, request, "/", "id")


    def test_edit_article_page_can_send_correct_form(self):
        self.mock_get.return_value = "ARTICLE"
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(edit_article, request, {"form": "FORM"}, "id")
        self.mock_get.assert_called_with(id="id")
        self.mock_form.assert_called_with(instance="ARTICLE")


    def test_can_raise_404_article(self):
        self.mock_get.side_effect = Article.DoesNotExist
        request = self.make_request("---", loggedin=True)
        with self.assertRaises(Http404):
            edit_article(request, "abc")
        self.mock_get.assert_called_with(id="abc")


    def test_edit_article_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        self.check_view_redirects(edit_article, request, "/writing/xxx/", "xxx")


    def test_edit_article_can_edit_article(self):
        self.mock_get.return_value = "ARTICLE"
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"z": "a"}, loggedin=True
        )
        edit_article(request, "abc")
        self.mock_get.assert_called_with(id="abc")
        self.mock_form.assert_called_with(QueryDict("z=a&id=abc"), instance="ARTICLE")
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_edit_article_view_can_delete_article(self):
        request = self.make_request(
         "---", method="post", data={"delete": "yes"}, loggedin=True
        )
        pub = Mock()
        self.mock_get.return_value = pub
        self.check_view_redirects(edit_article, request, "/writing/", "xxx")
        pub.delete.assert_called_with()
        self.mock_get.assert_called_with(id="xxx")



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



class NewBlogPostViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.BlogPostForm")
        self.mock_form = self.patcher2.start()


    def tearDown(self):
        self.patcher2.stop()
        ViewTest.tearDown(self)


    def test_new_blog_view_uses_new_blog_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(new_blog, request, "new-blog.html")


    def test_new_blog_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(new_blog, request, "/")


    def test_new_blog_sends_fresh_form(self):
        self.mock_form.return_value = "FORM"
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(new_blog, request, {"form": "FORM"})
        self.mock_form.assert_called_with()


    def test_new_blog_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"date": "2001-02-03"}, loggedin=True
        )
        self.check_view_redirects(new_blog, request, "/blog/2001/02/03/")


    def test_new_blog_can_create_blog_post(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = True
        request = self.make_request(
         "---", method="post", data={"date": "x-x-x", "b": "C"}, loggedin=True
        )
        new_blog(request)
        self.mock_form.assert_called_with(QueryDict("date=x-x-x&b=C"))
        form.is_valid.assert_called_with()
        form.save.assert_called_with()


    def test_new_blog_post_validation(self):
        form = Mock()
        self.mock_form.return_value = form
        form.is_valid.return_value = False
        request = self.make_request(
         "---", method="post", data={"date": "x-x-x", "b": "C"}, loggedin=True
        )
        self.check_view_uses_template(new_blog, request, "new-blog.html")
        self.check_view_has_context(new_blog, request, {"form": form})
        self.mock_form.assert_called_with(QueryDict("date=x-x-x&b=C"))
        form.is_valid.assert_called_with()



class BlogPostViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher2 = patch("samireland.views.BlogPost.objects.get")
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
        self.mock_get.assert_called_with(date="1000-20-30")


    def test_can_get_404_blog_post(self):
        self.mock_get.side_effect = BlogPost.DoesNotExist
        request = self.make_request("---")
        with self.assertRaises(Http404):
            blog_post(request, "1000", "20", "30")
        self.mock_get.assert_called_with(date="1000-20-30")



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
        self.patcher2 = patch("samireland.views.MediaFile.objects.create")
        self.patcher3 = patch("samireland.views.MediaFile.objects.all")
        self.patcher4 = patch("samireland.views.MediaFile.objects.get")
        self.mock_create = self.patcher2.start()
        self.mock_all = self.patcher3.start()
        self.mock_get = self.patcher4.start()
        self.media_file = SimpleUploadedFile("test.png", b"\x00\x01\x02\x03")


    def tearDown(self):
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        ViewTest.tearDown(self)


    def test_media_view_uses_media_template(self):
        request = self.make_request("---", loggedin=True)
        self.check_view_uses_template(media, request, "media.html")


    def test_media_page_is_protected(self):
        request = self.make_request("---")
        self.check_view_redirects(media, request, "/")


    def test_media_view_redirects_on_post(self):
        request = self.make_request("---", method="post", loggedin=True, data={
         "file": self.media_file, "name":"Test"
        })
        self.check_view_redirects(media, request, "/media/")


    def test_media_view_can_create_media(self):
        request = self.make_request("---", method="post", loggedin=True, data={
         "file": self.media_file, "name":"Test"
        })
        media(request)
        args, kwargs = self.mock_create.call_args_list[0]
        self.assertEqual(len(kwargs), 2)
        self.assertEqual(kwargs["name"], "Test")
        self.assertEqual(str(kwargs["mediafile"]), "test.png")


    def test_media_view_can_send_media(self):
        self.mock_all.return_value = [1, 2, 3]
        request = self.make_request("---", loggedin=True)
        self.check_view_has_context(media, request, {"media": [1, 2, 3]})
        self.mock_all.assert_called_with()


    def test_media_view_can_reject_duplicate_media_name(self):
        self.mock_create.side_effect = IntegrityError
        self.mock_all.return_value = [1, 2, 3]
        request = self.make_request("---", method="post", loggedin=True, data={
         "file": self.media_file, "name":"Test"
        })
        self.check_view_uses_template(media, request, "media.html")
        self.check_view_has_context(media, request, {
         "media": [1, 2, 3], "error": "There is already media with that name"
        })


    @patch("os.remove")
    def test_media_view_redirects_on_deletion(self, mock_remove):
        request = self.make_request("---", method="post", loggedin=True, data={
         "delete": "yes", "name": "media-name"
        })
        self.check_view_redirects(media, request, "/media/")


    @patch("os.remove")
    def test_media_view_can_delete_media(self, mock_remove):
        image = Mock()
        image_file = Mock()
        image.mediafile = image_file
        image_file.path = "PATH"
        self.mock_get.return_value = image
        request = self.make_request("---", method="post", loggedin=True, data={
         "delete": "yes", "name": "media-name"
        })
        media(request)
        self.mock_get.assert_called_with(name="media-name")
        image.delete.assert_called_with()
        mock_remove.assert_called_with("PATH")



class LoginViewTests(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("django.contrib.auth.authenticate")
        self.patcher2 = patch("django.contrib.auth.login")
        self.mock_auth = self.patcher1.start()
        self.mock_login = self.patcher2.start()
        self.mock_auth.return_value = "USER"


    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()


    def test_login_view_uses_login_template(self):
        request = self.make_request("---")
        self.check_view_uses_template(login, request, "login.html")


    def test_login_view_redirects_on_post(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        self.check_view_redirects(login, request, "/")


    def test_login_view_logs_in(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        login(request)
        self.mock_auth.assert_called_with(username="sam", password="pass")
        self.mock_login.assert_called_with(request, "USER")


    def test_login_view_sends_error_on_auth_failure(self):
        request = self.make_request(
         "---", method="post", data={"username": "sam", "password": "pass"}
        )
        self.mock_auth.return_value = None
        login(request)
        self.mock_auth.assert_called_with(username="sam", password="pass")
        self.assertFalse(self.mock_login.called)
        self.check_view_uses_template(login, request, "login.html")



class LogoutViewTests(TestCase, TestCaseX):

    @patch("django.contrib.auth.logout")
    def test_logout_view_redirects_home(self, mock_logout):
        request = self.make_request("---")
        self.check_view_redirects(logout, request, "/")


    @patch("django.contrib.auth.logout")
    def test_logout_view_logs_out(self, mock_logout):
        request = self.make_request("---")
        logout(request)
        mock_logout.assert_called()



class EditViewTests(TestCase, TestCaseX):

    def setUp(self):
        self.patcher1 = patch("samireland.views.EditableText.objects.get")
        self.mock_get = self.patcher1.start()
        self.mock_text = Mock()
        self.mock_text.body = "---"
        self.mock_get.return_value = self.mock_text


    def tearDown(self):
        self.patcher1.stop()


    def test_edit_view_returns_404_with_get(self):
        request = self.make_request("---", loggedin=True)
        with self.assertRaises(Http404):
            edit(request, "home")


    def test_edit_view_returns_404_with_unauthorised_post(self):
        request = self.make_request("---", method="post")
        with self.assertRaises(Http404):
            edit(request, "home")


    def test_redirects_to_specified_url(self):
        request = self.make_request("---", method="post", data={
         "redirect": "/login/", "body": "..."
        }, loggedin=True)
        self.check_view_redirects(edit, request, "/login/", "home")


    def test_can_update_editable_text(self):
        request = self.make_request("---", method="post", data={
         "redirect": "/login/", "body": "..."
        }, loggedin=True)
        edit(request, "home")
        self.mock_get.assert_called_with(name="home")
        self.assertEqual(self.mock_text.body, "...")
        self.mock_text.save.assert_called()



class EditableTextGrabberTests(TestCase):

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
