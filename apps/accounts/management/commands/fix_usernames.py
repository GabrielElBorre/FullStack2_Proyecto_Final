from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.accounts.models import CustomUser


class Command(BaseCommand):
    help = "Asigna username=email a usuarios que lo tengan vacío (corrige errores del admin)."

    def handle(self, *args, **options):
        actualizados = 0
        for user in CustomUser.objects.filter(Q(username__isnull=True) | Q(username="")):
            user.username = user.email
            user.save(update_fields=["username"])
            actualizados += 1
            self.stdout.write(f"Actualizado: {user.email}")

        self.stdout.write(self.style.SUCCESS(f"Listo. {actualizados} usuario(s) corregido(s)."))
