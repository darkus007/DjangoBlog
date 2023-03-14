"""
Тест urls приложения api.

"""
import logging

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from blog.models import Category, Post

User = get_user_model()


class UrlsTestCase(TestCase):   # python manage.py test api.tests.test_urls.UrlsTestCase
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')
        cls.admin = User.objects.create_superuser(username='admin', password='admin_password')

        cls.category = Category.objects.create(
            title='Тест категории',
            slug='test_category'
        )

        cls.post = Post.objects.create(
            user=cls.user,
            cat=cls.category,
            title='Название статьи',
            slug='nazvanie-stati',
            body='Текст статьи',
        )

        cls.client = Client()
        cls.auth_client = Client()
        cls.admin_client = Client()

        cls.auth_client.force_login(cls.user)
        cls.admin_client.force_login(cls.admin)

        logging.getLogger('django.request').setLevel(logging.ERROR)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None

    def test_api_category_get(self):
        response = self.client.get(reverse('api-category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_category_post_unauth(self):
        response = self.client.post(reverse('api-category'), data={'title': 'Тест категории'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_category_post_not_admin(self):
        response = self.auth_client.post(reverse('api-category'), data={'title': 'Тест категории'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_category_post_admin(self):
        response = self.admin_client.post(reverse('api-category'), data={'title': 'Тест категории'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_post_detail(self):
        response = self.client.get(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_post_get_unauth(self):
        response = self.client.get(reverse('api-post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_post_post_unauth(self):
        response = self.client.post(reverse('api-post'), data={'title': 'Тест категории'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_post_post_auth(self):
        response = self.auth_client.post(reverse('api-post'), data={
            'cat': '1',
            'title': 'Тест категории',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
