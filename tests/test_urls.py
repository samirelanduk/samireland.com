from seleniumx import TestCaseX
from django.test import TestCase
import samireland.views as views

class UrlTests(TestCase, TestCaseX):

    def test_home_url(self):
        self.check_url_returns_view("/", views.home)


    def test_research_url(self):
        self.check_url_returns_view("/research/", views.research)


    def test_new_publication_url(self):
        self.check_url_returns_view("/research/new/", views.new_pub)


    def test_publication_url(self):
        self.check_url_returns_view("/research/ab-cd/", views.publication)


    def test_publication_edit_url(self):
        self.check_url_returns_view("/research/ab-cd/edit/", views.edit_pub)


    def test_projects_url(self):
        self.check_url_returns_view("/projects/", views.projects)


    def test_new_project_url(self):
        self.check_url_returns_view("/projects/new/", views.new_project)


    def test_project_edit_url(self):
        self.check_url_returns_view("/projects/23/edit/", views.edit_project)


    def test_writing_url(self):
        self.check_url_returns_view("/writing/", views.writing)


    def test_about_url(self):
        self.check_url_returns_view("/about/", views.about)


    def test_media_url(self):
        self.check_url_returns_view("/media/", views.media)


    def test_login_url(self):
        self.check_url_returns_view("/authenticate/", views.login)


    def test_logout_url(self):
        self.check_url_returns_view("/logout/", views.logout)


    def test_edit_url(self):
        self.check_url_returns_view("/edit/abc/", views.edit)
