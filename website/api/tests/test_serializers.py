from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Category, Post
from api.serializers import CategorySerializer, PostSerializer


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        # Обязательно для Django, иначе может подняться исключение
        # AttributeError: type object 'Settings' has no attribute 'cls_atomics'
        super().setUpClass()

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
            slug='nazvanie_stati',
            body='Текст статьи',
        )

        # добавляем лайк
        cls.post.likes.add(cls.user)
        cls.post.save()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


class CategorySerializerTestCase(Settings):
    """
    Тестируем CategorySerializer.
    """
    # Для запуска только этого теста:
    # python manage.py test api.tests.test_serializers.CategorySerializerTestCase

    def test_ok(self):
        data = CategorySerializer(self.category).data
        self.assertEqual(data, {'id': 1, 'slug': 'test_category', 'title': 'Тест категории'})


class PostSerializerTestCase(Settings):
    """
    Тестируем PostSerializer.
    """
    # Для запуска только этого теста:
    # python manage.py test api.tests.test_serializers.PostSerializerTestCase

    def test_ok(self):
        data = PostSerializer(self.post).data
        expected_data = {'id': 1, 'user': 'test_user', 'cat': 1, 'title': 'Название статьи',
                         'slug': 'nazvanie_stati', 'body': 'Текст статьи',
                         'time_created': self.post.time_created.isoformat().replace("+00:00", "Z"),
                         'likes': [1]}
        self.assertEqual(data, expected_data)
