from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.campaigns.models import Campaign
from apps.donations.models import Donation

from .forms import CustomUserCreationForm, ProfileEditForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("accounts:login")


class LoginView(auth_views.LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = "account/logout.html"
    next_page = reverse_lazy("campaigns:list")


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "account/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset.html"
    email_template_name = "account/password_reset_email.html"
    html_email_template_name = "account/password_reset_email_html.html"
    subject_template_name = "account/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        campanas = Campaign.objects.filter(creador=user).annotate(
            num_donaciones=Count("donaciones")
        )
        donaciones = (
            Donation.objects.filter(usuario=user)
            .select_related("campana", "campana__creador")
            .order_by("-fecha_donacion")
        )
        totales = donaciones.aggregate(
            total=Sum("monto"),
            cantidad=Count("id"),
        )
        context.update(
            {
                "campanas_creadas": campanas,
                "donaciones": donaciones,
                "total_donado": totales["total"] or Decimal("0.00"),
                "cantidad_donaciones": totales["cantidad"] or 0,
                "tab_activa": self.request.GET.get("tab", "resumen"),
            }
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = "account/profile_edit.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(self.request, "Tu perfil se actualizó correctamente.")
        return super().form_valid(form)
