from django.conf import settings as project_settings
from django.core.cache import cache

from .models import Product


def get_products_by_category(category_id: int) -> list:
    """Возвращает список опубликованных продуктов указанной категории.

    Задание 3: сервисная функция для работы с продуктами.
    Задание 4: низкоуровневое кеширование с ключом category_{id}
    и временем жизни CACHE_TTL секунд.
    """
    key = f"category_{category_id}"
    products = cache.get(key)

    if products is None:
        products = list(
            Product.objects.filter(category_id=category_id, is_published=True)
            .select_related("category")
        )
        cache.set(key, products, timeout=project_settings.CACHE_TTL)

    return products