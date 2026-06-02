from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.donations.forms import DonationForm

from .forms import CampaignForm
from .models import Campaign


class CampaignListView(ListView):
    model = Campaign
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campanas"
    paginate_by = 9

    def get_queryset(self):
        queryset = Campaign.objects.filter(activa=True).select_related("creador")
        consulta = self.request.GET.get("q", "").strip()
        if consulta:
            queryset = queryset.filter(
                Q(nombre__icontains=consulta) | Q(descripcion__icontains=consulta)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consulta"] = self.request.GET.get("q", "")
        return context


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = "campaigns/campaign_detail.html"
    context_object_name = "campana"

    def get_queryset(self):
        return super().get_queryset().select_related("creador")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["donation_form"] = DonationForm()
        user = self.request.user
        context["puede_editar_campana"] = (
            user.is_authenticated and self.object.usuario_puede_editar(user)
        )
        context["puede_eliminar_campana"] = (
            user.is_authenticated and user.es_administrador
        )
        context["ultimas_donaciones"] = (
            self.object.donaciones.select_related("usuario").order_by("-fecha_donacion")[:8]
        )
        return context


class CanCreateCampaignMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.puede_crear_campanas


class CampaignCreateView(LoginRequiredMixin, CanCreateCampaignMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"

    def form_valid(self, form):
        form.instance.creador = self.request.user
        messages.success(
            self.request,
            f"Campaña creada. Apareces como organizador en tu perfil y en la página pública.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"

    def test_func(self):
        return self.get_object().usuario_puede_editar(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Campaña actualizada correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Campaign
    template_name = "campaigns/campaign_confirm_delete.html"
    success_url = reverse_lazy("campaigns:list")

    def test_func(self):
        return self.request.user.es_administrador

    def form_valid(self, form):
        messages.success(self.request, "Campaña eliminada correctamente.")
        return super().form_valid(form)
