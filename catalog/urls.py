from django.urls import path
from . import views

"""
URL-маршруты приложения catalog.
Связывает URL-адреса с представлениями (views) для отображения страниц сайта.
"""

urlpatterns = [
    # Главная страница магазина (каталог товаров)
    path('', views.home, name='home'),

    # Страница контактов с формой обратной связи
    path('contacts/', views.contacts, name='contacts'),
]
