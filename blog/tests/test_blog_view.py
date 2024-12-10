from unittest import TestCase
from unittest.mock import patch, MagicMock
from django.test import Client, RequestFactory
import pytest
from django.urls import reverse
from blog.views import home
from authentication.models import User


@pytest.mark.django_db
class HomeViewTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.client = Client()

        # self.photo1 = models.Photo.objects.create(title='Photo 1')
        # self.photo2 = models.Photo.objects.create(title='Photo 2')
        # self.blog1 = models.Blog.objects.create(title='Blog 1')
        # self.blog2 = models.Blog.objects.create(title='Blog 1')

    @pytest.mark.django_db
    def test_home_view_needs_to_be_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(302, response.status_code)

    @pytest.mark.django_db
    def test_logging_in_does_redirect_the_user_to_home(self):
        self.client.get(reverse('home'))
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.client.logout()
        self.assertEqual(200, response.status_code)
