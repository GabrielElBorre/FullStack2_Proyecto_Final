import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=200)),
                ("descripcion", models.TextField()),
                ("meta_recaudacion", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "recaudado_actual",
                    models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10),
                ),
                ("activa", models.BooleanField(default=True)),
                ("imagen", models.ImageField(blank=True, null=True, upload_to="campaigns/")),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                (
                    "creador",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="campanas_creadas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "campaña",
                "verbose_name_plural": "campañas",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]
