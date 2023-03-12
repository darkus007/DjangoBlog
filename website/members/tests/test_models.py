"""
Тест models приложения members.

"""

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase

from members.models import Profile


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create_user(username='test_user', password='test_user_password')

        cls.profile = Profile.objects.create(
            user=cls.user,
            slug='user-profile',
            ya_url='ya-url',
            vk_url='vk-url',
            ok_url='ok-url',
            git_url='git-url',
            website_url='website-url',
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


class ProfileModelTestCase(Settings):
    def test_slug_field(self):
        """
        Если класс SlugField изменится на другой, проверяем,
        что поле уникально и проиндексировано.
        """
        self.assertTrue(self.profile._meta.get_field('slug').unique)
        self.assertTrue(self.profile._meta.get_field('slug').db_index)

    def test_slug_length_fail(self):
        """
        Проверяем исключение ValidationError при попытке сохранения
        полей title и slug больше 160 символов (200)
        """
        user = User.objects.create_user(username='test_user2', password='test_user_password2')
        prof = Profile(user=user, slug='user'*40)   # 200 > 160 allowed
        with self.assertRaises(ValidationError):
            prof.full_clean()
            prof.save()

    def test_slug_length_equal_username_length(self):
        """
        Поле slug формируется автоматически из <User.username + '-profile'>,
        выполняем проверку их корреляции.
        """
        self.assertEqual(self.user._meta.get_field('username').max_length + 10,
                         self.profile._meta.get_field('slug').max_length)

    def test_get_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(), '/members/profile/user-profile/')

