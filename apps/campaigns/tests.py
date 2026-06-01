from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import RolUsuario
from apps.campaigns.models import Campaign
from apps.donations.models import Donation

User = get_user_model()


class CampaignModelTest(TestCase):
    def test_creacion_campana(self):
        user = User.objects.create_user(
            email="creador@test.com",
            password="pass12345",
            first_name="C",
            last_name="R",
            rol=RolUsuario.CREADOR,
        )
        campana = Campaign.objects.create(
            nombre="Ayuda escolar",
            descripcion="Útiles para niños",
            meta_recaudacion=Decimal("1000.00"),
            creador=user,
        )
        self.assertEqual(str(campana), "Ayuda escolar")
        self.assertEqual(campana.porcentaje_recaudado, 0)


class DonationModelTest(TestCase):
    def test_creacion_donacion_actualiza_recaudado(self):
        user = User.objects.create_user(
            email="donante@test.com",
            password="pass12345",
            first_name="D",
            last_name="O",
        )
        campana = Campaign.objects.create(
            nombre="Salud",
            descripcion="Medicinas",
            meta_recaudacion=Decimal("500.00"),
        )
        Donation.objects.create(campana=campana, usuario=user, monto=Decimal("50.00"))
        campana.refresh_from_db()
        self.assertEqual(campana.recaudado_actual, Decimal("50.00"))


class CampaignViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.campana = Campaign.objects.create(
            nombre="Medio ambiente",
            descripcion="Reforestación",
            meta_recaudacion=Decimal("2000.00"),
        )

    def test_vista_lista_campanas(self):
        response = self.client.get(reverse("campaigns:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Medio ambiente")

    def test_vista_detalle_campana(self):
        url = reverse("campaigns:detail", kwargs={"pk": self.campana.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reforestación")


class AuthenticationTest(TestCase):
    def test_login_con_email(self):
        User.objects.create_user(
            email="login@test.com",
            password="secret123",
            first_name="L",
            last_name="G",
        )
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "login@test.com", "password": "secret123"},
        )
        self.assertEqual(response.status_code, 302)
