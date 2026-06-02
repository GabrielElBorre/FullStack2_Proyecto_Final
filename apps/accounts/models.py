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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def nombre_para_mostrar(self):
        nombre = self.get_full_name().strip()
        return nombre if nombre else self.email.split("@")[0]

    @property
    def iniciales(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.nombre_para_mostrar[:2].upper()

    @property
    def etiqueta_rol(self):
        return dict(RolUsuario.choices).get(self.rol, self.rol)

    @property
    def puede_donar(self):
        """Cualquier usuario activo puede donar, sin importar su rol."""
        return self.is_active

    @property
    def puede_crear_campanas(self):
        return self.rol in (RolUsuario.CREADOR, RolUsuario.ADMIN) or self.is_staff

    @property
    def es_administrador(self):
        return self.rol == RolUsuario.ADMIN or self.is_staff
