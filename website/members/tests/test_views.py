"""
Тест views приложения members.

"""

from django.conf import settings
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from captcha.conf import settings as captcha_settings

from members.models import Profile

User = get_user_model()


class ViewsTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        settings.SECRET_KEY = "some_secret_key!"    # до создания и регистрации пользователя
        # captcha_settings.CAPTCHA_TEST_MODE = True  # отключаем проверку captcha

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')

        # cls.client = Client()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.profile = Profile.objects.create(
            user=cls.user,
            slug='user-profile',
            bio='user bio',
            ya_url='ya-url',
            vk_url='vk-url',
            ok_url='ok-url',
            git_url='git-url',
            website_url='website-url',
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None
        # captcha_settings.CAPTCHA_TEST_MODE = False

    def test_create_user_profile_view(self):
        profiles_count = Profile.objects.count()  # текущее количество записей в Profile

        user = User.objects.create_user(username='test_user2', password='test_user_password2')
        auth_client = Client()
        auth_client.force_login(user)

        form_data = {
            # 'slug': 'user-profile',   # формируется автоматически "(self.request.user.username) + '-profile'"
            'bio': 'User info',
            'ya_url': 'ya-url',
            'vk_url': 'vk-url',
            'ok_url': 'ok-url',
            'git_url': 'git-url',
            'website_url': 'website-url',
        }
        # Отправляем POST-запрос
        response = auth_client.post(reverse('user-profile-create'),
                                    data=form_data,
                                    follow=True)
        if response.context.get('form'):    # покажет ошибки формы, если они есть
            print(f"\nОшибка при валидации формы: {response.context.get('form').errors}")

        self.assertRedirects(response, '/members/profile/testuser2-profile/')  # Проверяем, сработал ли редирект
        self.assertEqual(Profile.objects.count(), profiles_count + 1)  # Проверяем, увеличилось ли число профайлов

    def test_edit_user_profile_view(self):
        profiles_count = Profile.objects.count()  # текущее количество записей в Profile

        form_data = {
            # 'user': self.user,    # пользователь добавляется автоматически при валидации
            'bio': 'User bio2',
            'ya_url': 'ya-url2',
            'vk_url': 'vk-url2',
            'ok_url': 'ok-url2',
            'git_url': 'git-url2',
            'website_url': 'website-url2',
        }
        # Отправляем POST-запрос
        response = self.auth_client.post(reverse('user-profile-update', kwargs={'slug': 'user-profile'}),
                                         data=form_data,
                                         follow=True)
        if response.context.get('form'):
            # покажет ошибки формы
            print(f"\nОшибка при валидации формы: {response.context.get('form').errors}")

        self.user.profile.refresh_from_db()

        # проверяем применение изменений в полях, которые передали
        user_to_dict = model_to_dict(self.user.profile)
        for key, value in form_data.items():
            self.assertEqual(user_to_dict[key], value)

        self.assertRedirects(response, reverse('home'))  # Проверяем, сработал ли редирект
        self.assertEqual(Profile.objects.count(), profiles_count)  # Проверяем неизменность количества профайлов
