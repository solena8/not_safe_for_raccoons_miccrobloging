from unittest import TestCase
from unittest.result import failfast

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.sql.datastructures import Empty
from django.test import Client
import pytest
from django.urls import reverse

from blog import models
from authentication.models import User
from conftest import test_user


@pytest.mark.django_db
class HomeViewTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

        self.small_gif = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                          b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                          b'\x02\x4c\x01\x00\x3b')

        self.photo1 = models.Photo.objects.create(
            image=SimpleUploadedFile('small1.gif', self.small_gif, content_type='image/gif'),
            caption='Photo 1',
            uploader=self.user
        )
        self.photo2 = models.Photo.objects.create(
            image=SimpleUploadedFile('small2.gif', self.small_gif, content_type='image/gif'),
            caption='Photo 2',
            uploader=self.user
        )
        self.blog1 = models.Blog.objects.create(title='Test Blog 1', content='Test 1', author=self.user,
                                                date_created='2023-01-15', starred=False)
        self.blog2 = models.Blog.objects.create(title='Test Blog 2', content='Test 2', author=self.user,
                                                date_created='2023-01-15', starred=False)

    # def tearDown(self):

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

    def test_home_view_displays_the_correct_amount_of_blogs(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['blogs']), 2)

    def test_home_view_displays_blogs_ordered_by_creation_date(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        blogs = response.context['blogs']
        self.assertTrue(blogs[0].date_created > blogs[1].date_created)

    def test_home_view_with_no_content(self):
        models.Blog.objects.all().delete()
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(reverse('home'), follow=True)
        self.assertNotIn('blogs', response.context)
