from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_('Название'),
        help_text=_('Введите название категории'),
        default='Без названия'  # Значение по умолчанию
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('URL-адрес'),
        help_text=_('Уникальный URL-адрес категории')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name=_('Категория')
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_('Название')
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        verbose_name=_('URL-адрес')
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name=_('Изображение')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_('Цена')
    )
    stock = models.PositiveIntegerField(
        verbose_name=_('Количество на складе')
    )
    available = models.BooleanField(
        default=True,
        verbose_name=_('Доступен')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])