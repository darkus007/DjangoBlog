# Generated by Django 4.1.5 on 2023-03-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=160, unique=True, verbose_name='URL'),
        ),
    ]
