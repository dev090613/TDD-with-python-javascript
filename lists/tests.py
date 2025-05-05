from django.test import TestCase
from django.http import HttpRequest
from .views import home_page


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):

        response = self.client.get("/")
        self.assertContains("<title>To-Do lists</title>", response)
        self.assertContains("<html>", response)
        self.assertContains("</html>", response)
