from django.core.management.base import BaseCommand

from apps.accounts.models import CustomUser, RolUsuario


class Command(BaseCommand):
    help = "Crea usuarios de prueba para demostración y evaluación."

    def _asegurar_usuario(self, email, password, first_name, last_name, rol, staff=False, superuser=False):
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "rol": rol,
                "is_staff": staff,
                "is_superuser": superuser,
            },
        )
        user.first_name = first_name
        user.last_name = last_name
        user.rol = rol
        user.is_staff = staff
        user.is_superuser = superuser
        user.username = email
        user.set_password(password)
        user.save()

        accion = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Usuario {accion}: {email}"))
        return user

    def handle(self, *args, **options):
        self._asegurar_usuario(
            "sebasborrego1@gmail.com",
            "Donaciones123",
            "Sebastian",
            "Borrego",
            RolUsuario.ADMIN,
            staff=True,
            superuser=True,
        )
        self._asegurar_usuario(
            "admin@donaciones.com",
            "admin123",
            "Admin",
            "Sistema",
            RolUsuario.ADMIN,
            staff=True,
            superuser=True,
        )
        self._asegurar_usuario(
            "usuario@test.com",
            "testpass123",
            "Usuario",
            "Prueba",
            RolUsuario.DONANTE,
        )
        self._asegurar_usuario(
            "sebasborrego0@gmail.com",
            "testpass123",
            "Sebastian",
            "Borrego",
            RolUsuario.CREADOR,
        )
        self._asegurar_usuario(
            "alu.21130555@correo.itlalaguna.edu.mx",
            "testpass123",
            "Alumno",
            "ITL",
            RolUsuario.DONANTE,
        )
