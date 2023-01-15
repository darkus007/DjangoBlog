from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='Автор поста')
    cat = models.ForeignKey(Category, on_delete=models.SET(1),
                            related_name='category', verbose_name='Категория')  # первая кат-рия будет "Разное"
    title = models.CharField(max_length=255, verbose_name='Наименование поста')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    body = models.TextField(verbose_name='Текст поста')
    time_created = models.DateTimeField(auto_now=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.title} - {self.user}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-time_created', 'cat']
