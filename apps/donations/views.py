from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from apps.campaigns.models import Campaign

from .forms import DonationForm
from .models import Donation


class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = "donations/donation_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.campana = get_object_or_404(Campaign, pk=kwargs["campana_pk"], activa=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campana"] = self.campana
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.campana = self.campana
        messages.success(self.request, "¡Gracias por tu donación!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("campaigns:detail", kwargs={"pk": self.campana.pk})


class MyDonationsListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = "donations/my_donations.html"
    context_object_name = "donaciones"
    paginate_by = 10

    def get_queryset(self):
        return Donation.objects.filter(usuario=self.request.user).select_related("campana")
