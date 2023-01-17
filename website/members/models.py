from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(null=True, blank=True, upload_to="avatars/%Y/%m/%d", verbose_name='Изображение')
    bio = models.TextField(verbose_name='О себе')
    ya_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Яндекс')
    vk_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='ВКонтакте')
    ok_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Одноклассники')
    git_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Git')
    website_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Website')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Инфо пользователя "О себе"'
        verbose_name_plural = 'Инфо пользователей "О себе"'
