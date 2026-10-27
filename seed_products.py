import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CardFlux.settings')
django.setup()

from catalog.models import Product

Product.objects.all().delete()

test_products = [
    {'name': 'Футболка базовая', 'description': 'Хлопок 100%, чёрный цвет', 'price': 1290},
    {'name': 'Кружка с принтом', 'description': 'Керамика, объём 330 мл', 'price': 590},
    {'name': 'Блокнот А5', 'description': 'Твёрдая обложка, 80 листов', 'price': 350},
]

for p in test_products:
    Product.objects.create(**p)

print(f'Создано товаров: {len(test_products)}')