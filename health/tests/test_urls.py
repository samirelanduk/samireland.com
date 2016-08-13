from django.core.urlresolvers import resolve, Resolver404
from django.test import TestCase
from health import views

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)


    def test_health_edit_url_resolves_to_health_edit_view(self):
        self.check_url_returns_view("/health/edit/", views.edit_page)


    def test_health_muscle_url_resolves_to_health_muscle_view(self):
        self.check_url_returns_view("/health/edit/musclegroup/xxx/", views.musclegroup_page)
