from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.accounts.models import CustomUser, RolUsuario
from apps.campaigns.models import Campaign


class Command(BaseCommand):
    help = "Crea campañas de demostración para pruebas y exposición."

    def handle(self, *args, **options):
        admin, _ = CustomUser.objects.get_or_create(
            email="admin@donaciones.com",
            defaults={"first_name": "Admin", "last_name": "Sistema", "rol": RolUsuario.ADMIN},
        )

        demos = [
            {
                "nombre": "Útiles escolares 2026",
                "descripcion": "Apoya a estudiantes de comunidades rurales con mochilas y útiles.",
                "meta_recaudacion": Decimal("5000.00"),
            },
            {
                "nombre": "Reforestación urbana",
                "descripcion": "Plantación de árboles en parques y zonas verdes de la ciudad.",
                "meta_recaudacion": Decimal("10000.00"),
            },
            {
                "nombre": "Banco de alimentos",
                "descripcion": "Donaciones para familias en situación de vulnerabilidad alimentaria.",
                "meta_recaudacion": Decimal("7500.00"),
            },
        ]

        for data in demos:
            campana, created = Campaign.objects.get_or_create(
                nombre=data["nombre"],
                defaults={
                    **data,
                    "creador": admin,
                    "recaudado_actual": Decimal("0.00"),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Campaña creada: {campana.nombre}"))
            else:
                self.stdout.write(f"Ya existe: {campana.nombre}")
