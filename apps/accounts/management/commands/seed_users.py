from django.core.management.base import BaseCommand

from apps.accounts.models import CustomUser, RolUsuario


class Command(BaseCommand):
    help = "Crea usuarios de prueba para demostración y evaluación."

    def handle(self, *args, **options):
        admin_user, created = CustomUser.objects.get_or_create(
            email="admin@donaciones.com",
            defaults={
                "first_name": "Admin",
                "last_name": "Sistema",
                "rol": RolUsuario.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superusuario creado: admin@donaciones.com"))
        else:
            admin_user.set_password("admin123")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.rol = RolUsuario.ADMIN
            admin_user.save()
            self.stdout.write("Superusuario actualizado: admin@donaciones.com")

        normal_user, created = CustomUser.objects.get_or_create(
            email="usuario@test.com",
            defaults={
                "first_name": "Usuario",
                "last_name": "Prueba",
                "rol": RolUsuario.DONANTE,
            },
        )
        if created:
            normal_user.set_password("testpass123")
            normal_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario creado: usuario@test.com"))
        else:
            normal_user.set_password("testpass123")
            normal_user.save()
            self.stdout.write("Usuario actualizado: usuario@test.com")
