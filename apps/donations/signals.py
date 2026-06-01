from decimal import Decimal

from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Donation


def actualizar_recaudado(campana):
    total = campana.donaciones.aggregate(total=Sum("monto"))["total"] or Decimal("0.00")
    campana.recaudado_actual = total
    campana.save(update_fields=["recaudado_actual"])


@receiver(post_save, sender=Donation)
def donacion_guardada(sender, instance, **kwargs):
    actualizar_recaudado(instance.campana)


@receiver(post_delete, sender=Donation)
def donacion_eliminada(sender, instance, **kwargs):
    actualizar_recaudado(instance.campana)
