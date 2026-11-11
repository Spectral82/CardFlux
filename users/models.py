from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь: вход по email, дополнительные поля профиля."""

    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Аватар", upload_to="users/", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=35, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

