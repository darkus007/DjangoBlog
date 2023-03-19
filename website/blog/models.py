from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
# стандартная библиотека не работает с русскими символами, потому используем свою
from website.utilites import slugify


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
    cat = models.ForeignKey(Category, on_delete=models.SET(1),  # первая кат-рия будет "Разное" задается в настройках
                            related_name='category', verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    body = RichTextField(blank=True, null=True, verbose_name='Текст статьи')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    likes = models.ManyToManyField(User, related_name='like')

    def __str__(self):
        return f'{self.title} - {self.user}'

    def save(self, *args, **kwargs):
        """ Добавляем slug, если он не был передан """
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-time_created', 'cat']
