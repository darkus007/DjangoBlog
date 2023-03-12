"""
Тест views приложения blog.

"""

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from captcha.conf import settings as captcha_settings

from blog.models import Category, Post

User = get_user_model()


class ViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"    # до создания и регистрации пользователя
        captcha_settings.CAPTCHA_TEST_MODE = True  # отключаем проверку captcha

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')

        cls.client = Client()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        # Создаем тестовую запись в БД Категории
        cls.category = Category.objects.create(
            title='Тест категории',
            slug='test_category'
        )

        cls.post = []
        # Создаем тестовую запись в БД Статьи (Поста)
        for i in range(0, 27):
            cls.post.append(Post.objects.create(
                user=cls.user,
                cat=cls.category,
                title=f'Название статьи {i}',
                slug=f'nazvanie-stati-{i}',
                body=f'Текст статьи {i}',
            ))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None
        captcha_settings.CAPTCHA_TEST_MODE = False

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        expected_all_categories = {'title': 'Все категории', 'slug': 'all-categories'}
        self.assertTrue(response.context.get('object_list'))    # object_list не пуст
        self.assertEqual(response.context.get('all_categories'), expected_all_categories)

    def test_post_detail_view(self):
        # response = self.client.get(reverse('post-detail'), kwargs={'slug': self.post[0].slug})
        response = self.client.get(f'/post/{self.post[0].slug}/')
        expected_object = {'title': self.post[0].title,
                           'slug': self.post[0].slug,
                           'body': self.post[0].body,
                           'time_created': self.post[0].time_created,
                           'user__username': self.post[0].user.username,
                           'cat__title': self.post[0].cat.title,
                           'user__id': self.post[0].user.id,
                           'user__first_name': self.post[0].user.first_name,
                           'user__last_name': self.post[0].user.last_name,
                           'user__profile__image': None,            # профиль пользователя не создавался
                           'user__profile__website_url': None,
                           'user__profile__git_url': None,
                           'user__profile__ya_url': None,
                           'user__profile__vk_url': None,
                           'user__profile__ok_url': None,
                           'user__profile__bio': None}
        self.assertEqual(response.context.get('object'), expected_object)

    def test_add_post_view(self):
        posts_count = Post.objects.count()  # текущее количество записей в Category
        form_data = {
            # 'user': self.user,    # пользователь добавляется автоматически при валидации
            'cat': 1,   # передаем 1, так как в форме используем widgets = {'cat': forms.Select ...
            'title': 'Тестовый пост 2',
            'slug': 'none',  # эмитируем поведение формы (widgets ...), slug формируется автоматически
            'body': 'Текст поста 2',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED'
        }
        # Отправляем POST-запрос
        response = self.auth_client.post(reverse('post-add'), data=form_data, follow=True)
        if response.context.get('form'):
            # покажет ошибки формы
            print(f"\nОшибка при валидации формы: {response.context.get('form').errors}")

        self.assertRedirects(response, reverse('home'))  # Проверяем, сработал ли редирект
        self.assertEqual(Post.objects.count(), posts_count + 1)  # Проверяем, увеличилось ли число постов

    def test_paginator(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context.get('object_list')), 25)
        response = self.client.get('/?page=2')
        self.assertEqual(len(response.context.get('object_list')), 2)
