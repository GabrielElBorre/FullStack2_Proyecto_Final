"""
Backend de correo: siempre muestra el mensaje en consola y, si hay credenciales
Gmail válidas en .env, también lo envía por SMTP.
"""
import logging

from django.conf import settings
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend

logger = logging.getLogger(__name__)


def _normalizar_app_password(password):
    return (password or "").strip().strip('"').replace(" ", "")


def _gmail_configurado():
    user = (settings.EMAIL_HOST_USER or "").strip()
    password = _normalizar_app_password(settings.EMAIL_HOST_PASSWORD)
    if not user or not password or len(password) < 16:
        return False
    placeholders = (
        "your-email",
        "example.com",
        "your-app-password",
        "tu-correo",
        "tu-clave",
        "pon_aqui",
        "contraseña_de_aplicacion",
    )
    credenciales = f"{user} {password}".lower()
    return not any(p in credenciales for p in placeholders)


class ConsoleAndGmailBackend(ConsoleEmailBackend):
    """Consola + Gmail (SMTP) cuando EMAIL_HOST_USER y EMAIL_HOST_PASSWORD están configurados."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._smtp_backend = None

    def _smtp(self):
        if self._smtp_backend is None:
            self._smtp_backend = SmtpEmailBackend(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER.strip(),
                password=_normalizar_app_password(settings.EMAIL_HOST_PASSWORD),
                use_tls=settings.EMAIL_USE_TLS,
                use_ssl=settings.EMAIL_USE_SSL,
                fail_silently=False,
                timeout=getattr(settings, "EMAIL_TIMEOUT", None),
            )
        return self._smtp_backend

    def send_messages(self, email_messages):
        # Siempre imprimir en consola (comportamiento actual)
        super().send_messages(email_messages)

        if not _gmail_configurado():
            pwd_len = len(_normalizar_app_password(settings.EMAIL_HOST_PASSWORD))
            logger.info(
                "Correo solo en consola: revisa EMAIL_HOST_USER y EMAIL_HOST_PASSWORD en .env "
                "(App Password de 16 caracteres, sin espacios). Longitud actual: %s",
                pwd_len,
            )
            return len(email_messages)

        try:
            enviados = self._smtp().send_messages(email_messages)
            logger.info("Correo enviado por Gmail SMTP a %s destinatario(s).", enviados)
            return enviados
        except Exception as exc:
            logger.exception("No se pudo enviar por Gmail (revisa App Password y .env): %s", exc)
            return 0
