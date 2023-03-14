"""
Тест views приложения api.

Проверяется чтение и добавление данных, запросы в БД.
Аутентификация проверяется в тестах urls.

"""
import logging

from django.conf import settings
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from blog.models import Category, Post

User = get_user_model()


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')
        cls.user2 = User.objects.create_user(username='test_user2', password='test_user_password2')
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
        cls.post1 = Post.objects.create(
            user=cls.user,
            cat=cls.category,
            title='Название статьи 1',
            slug='nazvanie-stati-1',
            body='Текст статьи 1',
        )
        cls.post2 = Post.objects.create(
            user=cls.user,
            cat=cls.category,
            title='Название статьи 2',
            slug='nazvanie-stati-2',
            body='Текст статьи 2',
        )

        cls.client = Client()
        cls.auth_client = Client()
        cls.not_author = Client()
        cls.admin_client = Client()

        cls.auth_client.force_login(cls.user)
        cls.not_author.force_login(cls.user2)
        cls.admin_client.force_login(cls.admin)

        logging.getLogger('django.request').setLevel(logging.ERROR)
        # loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None


class ApiCategoryViewsTestCase(Settings):  # python manage.py test api.tests.test_views.ApiCategoryViewsTestCase

    def test_api_category_get(self):
        response = self.client.get(reverse('api-category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), model_to_dict(self.category))

    def test_api_category_post(self):
        response = self.admin_client.post(reverse('api-category'),
                                          data={'title': 'Тест добавления категории'},
                                          content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 2,
                                         'slug': 'test-dobavleniya-kategorii',
                                         'title': 'Тест добавления категории'})

    def test_queries(self):
        """
        Тестируем количество запросов в БД при чтении категорий.
        """
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('api-category'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(queries), 1, "Увеличилось число запросов в БД!")

        # С увеличением записей в БД
        Category.objects.create(title='Тест категории 2', slug='test_category_2')

        # Количество запросов не увеличивается
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('api-category'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(queries), 1, "Увеличилось число запросов в БД!")


class ApiPostViewsTestCase(Settings):  # python manage.py test api.tests.test_views.ApiPostViewsTestCase

    def test_api_all_posts_get(self):
        expected_data = {'id': 1, 'user': 'test_user', 'cat': 1, 'title': 'Название статьи',
                         'slug': 'nazvanie-stati', 'body': 'Текст статьи',
                         'time_created': self.post.time_created.isoformat().replace("+00:00", "Z"),
                         'likes': []
                         }
        response = self.client.get(reverse('api-post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[2]), expected_data)

    def test_api_post_post_auth_user(self):
        response = self.auth_client.post(reverse('api-post'),
                                         data={'cat': '1', 'title': 'Тест добавления статьи'},
                                         content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Тест добавления статьи')

    def test_api_post_post_unauth_user(self):
        response = self.client.post(reverse('api-post'),
                                    data={'cat': '1', 'title': 'Тест добавления статьи'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_queries(self):
        """
        Тестируем количество запросов в БД при чтении статей (постов).
        """
        self.assertEqual(len(Post.objects.all()), 3)

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('api-post'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(queries), 2, "Увеличилось число запросов в БД!")

        # С увеличением записей в БД
        Post.objects.create(
            user=self.user,
            cat=self.category,
            title='Название статьи 4',
            slug='nazvanie-stati-4',
            body='Текст статьи 4',
        )
        self.assertEqual(len(Post.objects.all()), 4)

        # Количество запросов не увеличивается
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('api-post'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(queries), 2, "Увеличилось число запросов в БД!")


class ApiPostDetailViewsTestCase(Settings):  # python manage.py test api.tests.test_views.ApiPostDetailViewsTestCase

    def test_api_post_get(self):
        expected_data = {'id': 1, 'user': 'test_user', 'cat': 1, 'title': 'Название статьи',
                         'slug': 'nazvanie-stati', 'body': 'Текст статьи',
                         'time_created': self.post.time_created.isoformat().replace("+00:00", "Z"),
                         'likes': []
                         }
        response = self.client.get(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data), expected_data)

    def test_api_post_put_author(self):
        response = self.auth_client.put(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                        data={'title': 'Тест обновления статьи put'},
                                        content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тест обновления статьи put')

    def test_api_post_put_admin(self):
        response = self.admin_client.put(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                         data={'title': 'Тест обновления статьи put admin'},
                                         content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тест обновления статьи put admin')

    def test_api_post_put_not_author(self):
        response = self.not_author.put(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                       data={'title': 'Тест обновления статьи put'},
                                       content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'info': 'Обновить статью может только ее автор.'})

    def test_api_post_patch_author(self):
        response = self.auth_client.patch(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                          data={'title': 'Тест обновления статьи patch'},
                                          content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тест обновления статьи patch')

    def test_api_post_patch_admin(self):
        response = self.admin_client.patch(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                           data={'title': 'Тест обновления статьи patch admin'},
                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тест обновления статьи patch admin')

    def test_api_post_patch_not_author(self):
        response = self.not_author.patch(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}),
                                         data={'title': 'Тест обновления статьи put'},
                                         content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'info': 'Обновить статью может только ее автор.'})

    def test_api_delete_author(self):
        response = self.auth_client.delete(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati-2'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_admin(self):
        response = self.admin_client.delete(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati-2'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_not_author(self):
        response = self.not_author.delete(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati-2'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'info': 'Удалить статью может только ее автор.'})

    def test_queries(self):
        """
        Тестируем количество запросов в БД при чтении одной статьи (поста).
        """
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('api-post-detail', kwargs={'slug': 'nazvanie-stati'}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(queries), 2, "Увеличилось число запросов в БД!")
