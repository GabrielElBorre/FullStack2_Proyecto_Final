from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import RedirectView

from apps.campaigns.models import Campaign

from .forms import DonationForm
from .models import Donation


class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = "donations/donation_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.puede_donar:
            raise PermissionDenied("Tu cuenta no está activa para realizar donaciones.")
        self.campana = get_object_or_404(Campaign, pk=kwargs["campana_pk"], activa=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campana"] = self.campana
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.campana = self.campana
        messages.success(
            self.request,
            f"¡Gracias! Tu donación de {form.instance.monto} MXN quedó registrada en tu perfil.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("accounts:profile") + "?tab=donaciones"


class MyDonationsListView(LoginRequiredMixin, RedirectView):
    """Redirige al perfil, sección de donaciones."""

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:profile") + "?tab=donaciones"
