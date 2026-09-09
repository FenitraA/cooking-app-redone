from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default application roles"

    def handle(self, *args, **options):

        admin_group, _ = Group.objects.get_or_create(name="ADMIN")
        ingredient_manager_group, _ = Group.objects.get_or_create(
            name="INGREDIENT_MANAGER"
        )
        basic_group, _ = Group.objects.get_or_create(name="BASIC")
        reader_group, _ = Group.objects.get_or_create(name="READER")

        # ADMIN → everything
        admin_group.permissions.set(
            Permission.objects.all()
        )

        # READER → all view permissions
        reader_group.permissions.set(
            Permission.objects.filter(
                codename__startswith="view_"
            )
        )

        # BASIC → view + add + change everything EXCEPT ingredients
        basic_permissions = Permission.objects.filter(
            codename__regex=r"^(view_|add_|change_|delete_)"
        ).exclude(
            content_type__app_label="ingredients"
        )

        basic_group.permissions.set(basic_permissions)

        # INGREDIENT_MANAGER → view + add + change ingredients
        ingredient_permissions = Permission.objects.filter(
            codename__regex=r"^(view_|add_|change_|delete_)"
        )

        ingredient_manager_group.permissions.set(
            ingredient_permissions
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles and permissions configured successfully."
            )
        )