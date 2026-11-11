from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='catalog/', blank=True, null=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    is_active = models.BooleanField(default=True, verbose_name='Доступен')

    # Задание 1: статус публикации. По умолчанию товар НЕ опубликован.
    is_published = models.BooleanField("Опубликовано", default=False)

    # Задание 2: владелец продукта.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=50)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.created_at}"

    class Meta:
        verbose_name = "Сообщение из формы"
        verbose_name_plural = "Сообщения из формы"