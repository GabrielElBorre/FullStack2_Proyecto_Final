from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from django_project.email_backends import _gmail_configurado, _normalizar_app_password


class Command(BaseCommand):
    help = "Prueba el envío SMTP a Gmail (sin contraseña en la salida)."

    def add_arguments(self, parser):
        parser.add_argument(
            "destino",
            nargs="?",
            default=settings.EMAIL_HOST_USER,
            help="Correo destino (por defecto la cuenta de la plataforma)",
        )

    def handle(self, *args, **options):
        destino = options["destino"]
        pwd = _normalizar_app_password(settings.EMAIL_HOST_PASSWORD)
        self.stdout.write(f"Usuario SMTP: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"Longitud App Password: {len(pwd)} caracteres")
        self.stdout.write(f"Gmail configurado: {_gmail_configurado()}")

        if not _gmail_configurado():
            self.stderr.write(
                self.style.ERROR(
                    "Configuración incompleta. Usa App Password de 16 caracteres sin espacios en .env"
                )
            )
            return

        send_mail(
            subject="Prueba DonaAhora — correo SMTP",
            message="Si lees esto, Gmail SMTP funciona correctamente.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destino],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f"Correo de prueba enviado a {destino}"))
