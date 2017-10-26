from samireland.tests import UrlTest
from home import views

class HomeUrlTests(UrlTest):

    def test_home_page_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/", views.home_page)


    def test_about_page_url_resolves_to_about_page_view(self):
        self.check_url_returns_view("/about/", views.about_page)


    def test_research_page_url_resolves_to_research_page_view(self):
        self.check_url_returns_view("/research/", views.research_page)


    def test_new_research_page_url_resolves_to_new_research_page_view(self):
        self.check_url_returns_view("/research/new/", views.new_research_page)


    def test_publication_url_resolves_to_publication_page_view(self):
        self.check_url_returns_view("/research/pub-id/", views.publication_page)


    def test_edit_publication_url_resolves_to_edit_publication_page_view(self):
        self.check_url_returns_view("/research/pub-id/edit/", views.edit_publication_page)


    def test_project_page_url_resolves_to_project_page_view(self):
        self.check_url_returns_view("/projects/", views.projects_page)


    def test_login_url_resolves_to_login_view(self):
        self.check_url_returns_view("/authenticate/", views.login_page)


    def test_fence_url_resolves_to_fence_view(self):
        self.check_url_returns_view("/youshallnotpass/", views.fence_page)


    def test_logout_url_resolves_to_logout_view(self):
        self.check_url_returns_view("/logout/", views.logout_page)


    def test_edit_home_page_resolves_to_edit_home_view(self):
        self.check_url_returns_view("/edit/home/", views.edit_page)


    def test_edit_about_page_resolves_to_edit_about_view(self):
        self.check_url_returns_view("/edit/about/", views.edit_page)
