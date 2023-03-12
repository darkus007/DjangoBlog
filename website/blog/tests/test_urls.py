"""
Тест urls приложения blog.

Проверяем доступности url и используемые шаблоны.

На уровне view не используется разграничение доступа,
оно реализовано в шаблонах - предлагается перейти
на страницу регистрации или отправить e-mail администратору.
Автоматические перенаправления также не используются.

По этой причине нет тестов перенаправления и проверки доступа.
"""

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from blog.models import Category, Post

User = get_user_model()


class UrlsTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.client = Client()

        # Создаем пользователя для тестов
        cls.user = User.objects.create_user(username='test_user', password='test_user_password')

        # Создаем тестовую запись в БД Категории
        cls.category = Category.objects.create(
            title='Тест категории',
            slug='test_category'
        )

        # Создаем тестовую запись в БД Статьи (Поста)
        cls.post = Post.objects.create(
            user=cls.user,
            cat=cls.category,
            title='Название статьи',
            slug='nazvanie-stati',
            body='Текст статьи',
        )

        settings.SECRET_KEY = "some_secret_key!"

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/home.html', 'blog/paginator.html', 'blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_post_detail(self):
        response = self.client.get('/post/nazvanie-stati/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_post_add(self):
        response = self.client.get('/add-post/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_post_update(self):
        response = self.client.get('/update-post/nazvanie-stati/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_post_delete(self):
        response = self.client.get('/delete-post/nazvanie-stati/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_post_search(self):
        response = self.client.get('/post-search/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_user_posts(self):
        # авторизуем пользователя
        authorized_client = Client()
        authorized_client.force_login(self.user)

        response = authorized_client.get('/user-posts/')

        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_categories(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_category_add(self):
        response = self.client.get('/add-category/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_category_update(self):
        response = self.client.get('/update-category/test_category/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_category_delete(self):
        response = self.client.get('/delete-category/test_category/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_posts_by_category(self):
        response = self.client.get('/category/test_category/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_like_post(self):
        response = self.client.get('/like/test_category/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_send_email(self):
        response = self.client.get('/email/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)

    def test_email_success(self):
        response = self.client.get('/email-success/')
        self.assertEqual(response.status_code, 200)
        for template in ('blog/base.html', 'blog/categories_tag.html'):
            self.assertTemplateUsed(response, template)
