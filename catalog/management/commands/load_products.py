from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = "Загружает фикстуры с предварительным удалением существующих данных"

    def handle(self, *args, **options):
        self.stdout.write(" Удаляем существующие продукты и категории...")
        deleted_products = Product.objects.all().delete()
        deleted_categories = Category.objects.all().delete()

        self.stdout.write(
            f" Удалено: категорий={deleted_categories[0]}, продуктов={deleted_products[0]}"
        )

        self.stdout.write("🚀 Начинаем загрузку фикстуры fixtures.json...")
        call_command('loaddata', 'fixtures.json')

        self.stdout.write(self.style.SUCCESS(" Фикстура загружена успешно!"))