from django.conf import settings
from django.db import models

from apps.campaigns.models import Campaign


class Donation(models.Model):
    campana = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="donaciones",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donaciones",
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_donacion = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_donacion"]
        verbose_name = "donación"
        verbose_name_plural = "donaciones"

    def __str__(self):
        return f"{self.usuario.email} - ${self.monto} a {self.campana.nombre}"
