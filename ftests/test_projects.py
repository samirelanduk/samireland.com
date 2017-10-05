"""Contains tests for the projects section."""

from time import sleep
from random import randint
import datetime
from .base import FunctionalTest

class ProjectPageTests(FunctionalTest):

    def test_can_change_project_page_text(self):
        self.check_can_edit_text("/projects/", "projects-summary", "projects")


    def test_cannot_access_project_edit_page_when_not_logged_in(self):
        self.get("/edit/projects/")
        self.check_page("/")
