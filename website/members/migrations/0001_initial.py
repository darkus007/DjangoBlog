# Generated by Django 4.1.5 on 2023-01-16 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('image', models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/%d', verbose_name='Изображение')),
                ('bio', models.TextField(verbose_name='О себе')),
                ('ya_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Яндекс')),
                ('vk_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='ВКонтакте')),
                ('ok_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Одноклассники')),
                ('git_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Git')),
                ('website_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Инфо пользователя "О себе"',
                'verbose_name_plural': 'Инфо пользователей "О себе"',
            },
        ),
    ]
