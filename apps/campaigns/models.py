from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse


class Campaign(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    meta_recaudacion = models.DecimalField(max_digits=10, decimal_places=2)
    recaudado_actual = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    activa = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="campaigns/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campanas_creadas",
    )

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "campaña"
        verbose_name_plural = "campañas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("campaigns:detail", kwargs={"pk": self.pk})

    @property
    def porcentaje_recaudado(self):
        if self.meta_recaudacion <= 0:
            return 0
        porcentaje = (self.recaudado_actual / self.meta_recaudacion) * 100
        return min(float(porcentaje), 100.0)

    def usuario_puede_editar(self, user):
        if not user.is_authenticated:
            return False
        if user.es_administrador:
            return True
        return self.creador_id == user.pk and user.puede_crear_campanas
