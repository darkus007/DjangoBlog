from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from captcha.conf import settings as captcha_settings

from blog.forms import CategoryForm, PostForm
from blog.models import Category, Post

User = get_user_model()


class CategoryFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"  # до создания и регистрации пользователя

        Category.objects.create(
            title='Тестовая категория',
            slug='test-category'
        )
        cls.form = CategoryForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()

    def test_create_category(self):
        """ Валидная форма создает запись в Category. """

        categories_count = Category.objects.count()

        form_data = {
            'title': 'Тестовая категория 2',
            'slug': 'none'  # эмитируем поведение формы (widgets ...), slug формируется автоматически
        }

        response = self.guest_client.post(
            reverse('category-add'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('categories'))
        self.assertEqual(Category.objects.count(), categories_count + 1)
        self.assertTrue(
            Category.objects.filter(
                title='Тестовая категория 2',
                slug='testovaya-kategoriya-2'
            ).exists()
        )


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"

        captcha_settings.CAPTCHA_TEST_MODE = True   # отключаем проверку captcha

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.cat = Category.objects.create(
            title='Тестовая категория',
            slug='test-category'
        )

        cls.post = Post.objects.create(
            user=cls.user,
            cat=cls.cat,
            title='Тестовый пост',
            slug='test-post',
            body='Текст поста'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        captcha_settings.CAPTCHA_TEST_MODE = False

    def test_post_form(self):
        """ Проверка валидации формы Post и формирование slug."""

        form_data = {
            'cat': self.cat,
            'title': 'Тестовый пост 2',
            'slug': 'none',  # эмитируем поведение формы (widgets ...), slug формируется автоматически
            'body': 'Текст поста 2',
            'captcha_0': 'PASSED',
            'captcha_1': 'PASSED'
        }

        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.slug, 'testovyij-post-2')
        # print(f"{form.errors=}")      # посмотреть ошибки при валидации
