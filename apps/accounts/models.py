from django.contrib.auth.models import AbstractUser
from django.db import models


class RolUsuario(models.TextChoices):
    DONANTE = "donante", "Donante"
    CREADOR = "creador", "Creador de campañas"
    ADMIN = "admin", "Administrador"


class CustomUser(AbstractUser):
    """Usuario personalizado con email como identificador de inicio de sesión."""

    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField("correo electrónico", unique=True)
    rol = models.CharField(
        max_length=20,
        choices=RolUsuario.choices,
        default=RolUsuario.DONANTE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email

    @property
    def puede_crear_campanas(self):
        return self.rol in (RolUsuario.CREADOR, RolUsuario.ADMIN) or self.is_staff

    @property
    def es_administrador(self):
        return self.rol == RolUsuario.ADMIN or self.is_staff
