from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


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
    subject_template_name = "account/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"
