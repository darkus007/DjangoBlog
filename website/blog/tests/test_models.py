"""
Тест models приложения blog.

Тестируем методы моделей Category и Post,
некоторые настройки полей этих моделей.

Примечание:
При использовании методов класса setUpClass() и tearDownClass()
обязательно вызываем в них super(): super().setUpClass() и super().tearDownClass().
Без вызова super() все тесты сработают нормально, но получим ошибку:

AttributeError: type object '<имя_класса>' has no attribute 'cls_atomics'

Эта ошибка возникает именно в Django: в Unittest для Python такой проблемы нет.
"""

from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Category, Post


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')

        cls.category = Category.objects.create(
            title='Тест категории',
            slug='test_category'
        )

        cls.post = Post.objects.create(
            user=cls.user,
            cat=cls.category,
            title='Название статьи',
            slug='nazvanie_stati',
            body='Текст статьи',
        )

        cls.post.likes.add(cls.user)
        cls.post.save()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


class PostTestCase(Settings):
    def test_slug_field(self):
        """
        Если класс SlugField изменится на другой, проверяем,
        что поле уникально и проиндексировано.
        """
        self.assertTrue(self.post._meta.get_field('slug').unique)
        self.assertTrue(self.post._meta.get_field('slug').db_index)

    def test_verbose_name(self):
        """ verbose_name в полях совпадает с ожидаемым. """
        field_verboses = {
            'user': 'Автор поста',
            'cat': 'Категория',
            'title': 'Название статьи',
            'slug': 'URL',
            'body': 'Текст статьи',
            'time_created': 'Время создания',
            'likes': 'likes',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, expected_value)

    def test_auto_add_slug(self):
        post = Post.objects.create(
            user=self.user,
            cat=self.category,
            title='Название статьи 2',
            body='Текст статьи 2'
        )
        post.save()
        self.assertEqual(post.slug, 'nazvanie-stati-2')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/nazvanie_stati/')

    def test_total_likes(self):
        self.assertEqual(self.post.total_likes(), 1)

    def test_auto_time_created(self):
        """
        Проверка автозаполнения поля time_created
        и его принадлежность классу datetime.
        """
        self.assertTrue(isinstance(self.post.time_created, datetime))

    def test_str(self):
        self.assertEqual(f'{self.post.title} - {self.post.user}', self.post.__str__())


class CategoryTestCase(Settings):
    def test_fields(self):
        self.assertEqual(self.category.title, 'Тест категории')
        self.assertEqual(self.category.slug, 'test_category')
        self.assertEqual(self.category._meta.get_field('title').validators[0].limit_value, 255)
        self.assertEqual(self.category._meta.get_field('title').validators[0].message, '')
        self.assertEqual(self.category._meta.get_field('title').verbose_name, 'Название категории')

        self.assertEqual(self.category._meta.get_field('slug').verbose_name, 'URL')
        self.assertEqual(self.category._meta.get_field('slug').unique, True)
        self.assertEqual(self.category._meta.get_field('slug').db_index, True)

    def test_max_length_fail(self):
        """
        Проверяем исключение ValidationError при попытке сохранения
        полей title и slug больше 255 символов (300)
        """
        cat = Category(title='cat'*100, slug='cat'*100)
        with self.assertRaises(ValidationError):
            cat.full_clean()
            cat.save()

    def test_str(self):
        self.assertEqual(self.category.title, self.category.__str__())
