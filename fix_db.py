import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CardFlux.settings")
django.setup()

from django.db import connection

with connection.cursor() as cur:
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    tables = [row[0] for row in cur.fetchall()]
    print(f"Найдено таблиц: {len(tables)}")
    for table in tables:
        cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
    print("Все таблицы удалены. Теперь запустите: python manage.py migrate")