# Generated by Django 5.2.4 on 2025-07-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_name_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, default='Без названия', help_text='Введите название категории', max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Уникальный URL-адрес категории', max_length=200, unique=True, verbose_name='URL-адрес'),
        ),
    ]
