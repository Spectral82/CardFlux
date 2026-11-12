from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группу «Контент-менеджер» с правами на публикации блога."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Контент-менеджер")

        permissions = Permission.objects.filter(
            content_type__app_label="blog",
            content_type__model="blogpost",
            codename__in=["add_blogpost", "change_blogpost", "delete_blogpost", "view_blogpost"],
        )
        group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа «Контент-менеджер» создана."))
        else:
            self.stdout.write(self.style.SUCCESS(
                "Группа «Контент-менеджер» уже существует, права обновлены."
            ))

        for perm in permissions:
            self.stdout.write(f""
                              f"  - {perm.codename}")